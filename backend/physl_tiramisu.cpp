//  Copyright (c) 2019-2020 Christopher Taylor
//
//  Distributed under the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#include <isl/aff.h>
#include <isl/set.h>
#include <isl/map.h>
#include <isl/union_map.h>
#include <isl/union_set.h>
#include <isl/ast_build.h>
#include <isl/schedule.h>
#include <isl/schedule_node.h>
#include <isl/space.h>
#include <isl/constraint.h>

#include <isl/id.h>
#include <isl/val.h>
#include <isl_ast_private.h>

#include "physl_isl.hpp"

#include <tiramisu/debug.h>
#include <tiramisu/expr.h>
#include <tiramisu/type.h>
#include <tiramisu/computation_graph.h>
#include <tiramisu/core.h>

using namespace tiramisu;

namespace physl { namespace tiramisu {

// taken from `tiramisu_codegen_halide.cpp:2549`
//
static inline isl_ast_node *for_code_generator_after_for(isl_ast_node *node, isl_ast_build *build, void *user) {
    return node;
}

class PhyslFunction : public function, public generator {

    public:

    PhyslFunction() : function("physl_codgen"), generator() {}

    auto get_mapping() { return mapping; }
    void lift_dist() { lift_dist_comps(); }

    void generate_code(std::string &physlstr) {

        // Check that time_processor representation has already been computed,
        //
        //assert(get_trimmed_time_proc_dom() != nullptr);
        //assert(get_aligned_ident_schedules() != nullptr);

        isl_ctx *ctx = get_isl_ctx();
        assert(ctx != nullptr);
        isl_ast_build *ast_build = nullptr;

        // Rename updates so that they have different names because
        // the code generator expects each unique name to have
        // an expression, different computations that have the same
        // name cannot have different expressions.
        //
        rename_computations();

        if (get_program_context() == nullptr) {
            ast_build = isl_ast_build_alloc(ctx);
        }
        else {
            ast_build = isl_ast_build_from_context(isl_set_copy(this->get_program_context()));
        }

        isl_options_set_ast_build_atomic_upper_bound(ctx, 1);
        isl_options_get_ast_build_exploit_nested_bounds(ctx);
        isl_options_set_ast_build_group_coscheduled(ctx, 1);

        ast_build = isl_ast_build_set_after_each_for(ast_build, &for_code_generator_after_for,
                    nullptr);
        ast_build = isl_ast_build_set_at_each_domain(ast_build, &generator::stmt_code_generator,
                    this);

        // Set iterator names
        isl_id_list *iterators = isl_id_list_alloc(ctx, this->get_iterator_names().size());

        if (this->get_iterator_names().size() > 0)
        {
            std::string name = generate_new_variable_name();
            isl_id *id = isl_id_alloc(ctx, name.c_str(), NULL);
            iterators = isl_id_list_add(iterators, id);

            const auto iterator_names = get_iterator_names();
            const auto iterator_names_size = iterator_names.size();

            for (int i = 0; i < iterator_names_size; i++)
            {
                name = iterator_names[i];
                id = isl_id_alloc(ctx, name.c_str(), NULL);
                iterators = isl_id_list_add(iterators, id);

                name = generate_new_variable_name();
                id = isl_id_alloc(ctx, name.c_str(), NULL);
                iterators = isl_id_list_add(iterators, id);
            }

            ast_build = isl_ast_build_set_iterators(ast_build, iterators);
        }

        { // beg scope

            // Intersect the iteration domain with the domain of the schedule.
            isl_union_map *umap =
                isl_union_map_intersect_domain(
                    isl_union_map_copy(get_aligned_identity_schedules()),
                    isl_union_set_copy(get_trimmed_time_processor_domain()));

            isl_ast_node* ast = isl_ast_build_node_from_schedule_map(ast_build, umap);
            std::shared_ptr<isl_ast_node> ast_ptr{};
            ast_ptr.reset(ast);

            physl::codegen::generate_physl(ast_ptr, physlstr);

        } // end scope

        isl_ast_build_free(ast_build);
    }
};

//int codegen(const std::vector< std::shared_ptr<buffer> > &arguments, const bool gen_cuda_stmt, std::string & physlstr)
//
int codegen(const std::vector< std::shared_ptr<buffer> > &arguments, std::string & physlstr)
{
    std::vector<buffer *> bufs{};

    if(arguments.size()) {
        bufs.reserve(arguments.size());
        std::transform(arguments.begin(), arguments.end(), bufs.begin(), [](auto arg) { return arg.get(); });
    }

    PhyslFunction fct{}; // = global::get_implicit_function();

    { // begin scope

        /*
        if(gen_cuda_stmt)
        {
            if(!fct.get_mapping().empty())
            {
                tiramisu::computation* c1 = fct->get_first_cpt();
                tiramisu::computation* c2 = fct->get_last_cpt();
                Automatic_communication(c1,c2);
            }
            else {
                DEBUG(3, tiramisu::str_dump("You must specify the corresponding CPU buffer to each GPU buffer else you should do the communication manually"));
            }
        }
        */

        fct.set_arguments(bufs);
        fct.lift_dist();
        fct.gen_time_space_domain();
        fct.generate_code(physlstr);

        /*
        if (gen_cuda_stmt) {
            fct.gen_cuda_stmt();
        }

        fct.gen_halide_stmt();
        fct->gen_halide_obj(obj_filename);
        */

    } // end scope

    return 1;

} // end codegen

} /* end namespace tiramisu */ } // end namespace physl
