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

#include <isl/id.h>
#include <isl/val.h>
#include <isl/ast_type.h>

// this is required and can only be found in
// the source tree for isl
//
// this file is not installed as part of
// the isl build
//
#include "isl_ast_private.h"

#include "physl_isl.hpp"

#include <string>
#include <cstring>
#include <sstream>

#define isl_ast_op_last	isl_ast_op_address_of

namespace physl { namespace codegen {

__isl_give isl_printer *isl_ast_node_list_print__(
        __isl_keep isl_ast_node_list *list, __isl_take isl_printer *p,
        __isl_keep isl_ast_print_options *options);

/* Print the start of a compound statement.
 */
static __isl_give isl_printer *start_block(__isl_take isl_printer *p)
{
	p = isl_printer_start_line(p);
	p = isl_printer_print_str(p, "block(");
	p = isl_printer_end_line(p);
	p = isl_printer_indent(p, 2);

	return p;
}

/* Print the end of a compound statement.
 */
static __isl_give isl_printer *end_block(__isl_take isl_printer *p)
{
	p = isl_printer_indent(p, -2);
	p = isl_printer_start_line(p);
	p = isl_printer_print_str(p, ")");
	p = isl_printer_end_line(p);

	return p;
}

static int need_block(__isl_keep isl_ast_node *node)
{
	isl_ctx *ctx;

	if (node->type == isl_ast_node_block)
		return 1;
	if (node->type == isl_ast_node_for && node->u.f.degenerate)
		return 1;
	if (node->type == isl_ast_node_if && node->u.i.else_node)
		return 1;
	if (node->type == isl_ast_node_mark)
		return 1;

	ctx = isl_ast_node_get_ctx(node);
	return isl_options_get_ast_always_print_block(ctx);
}

/* Retrieve the note identified by "id" from "p".
 * The note is assumed to exist.
 */
static void *get_note(__isl_keep isl_printer *p, __isl_keep isl_id *id)
{
	void *note;

	id = isl_printer_get_note(p, isl_id_copy(id));
	note = isl_id_get_user(id);
	isl_id_free(id);

	return note;
}

/* Return the node marked by mark node "node".
 */
__isl_give isl_ast_node *isl_ast_node_mark_get_node(
	__isl_keep isl_ast_node *node)
{
	if (!node)
		return NULL;
	if (node->type != isl_ast_node_mark)
		isl_die(isl_ast_node_get_ctx(node), isl_error_invalid,
			"not a mark node", return NULL);

	return isl_ast_node_copy(node->u.m.node);
}

/* Data structure that holds the user-specified textual
 * representations for the operators in C format.
 * The entries are either NULL or copies of strings.
 * A NULL entry means that the default name should be used.
 */
struct isl_ast_op_names {
	char *op_str[isl_ast_op_last + 1];
};

/* Create an empty struct isl_ast_op_names.
 */
static void *create_names(isl_ctx *ctx)
{
	return isl_calloc_type(ctx, struct isl_ast_op_names);
}

/* Free a struct isl_ast_op_names along with all memory
 * owned by the struct.
 */
static void free_names(void *user)
{
	int i;
	struct isl_ast_op_names *names = static_cast<struct isl_ast_op_names *>(user);

	if (!user)
		return;

	for (i = 0; i <= isl_ast_op_last; ++i)
		free(names->op_str[i]);
	free(user);
}

/* Create an identifier that is used to store
 * an isl_ast_op_names note.
 */
static __isl_give isl_id *names_id(isl_ctx *ctx)
{
	return isl_id_alloc(ctx, "isl_ast_op_type_names", NULL);
}



static __isl_give isl_printer *print_ast_node_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_node *node,
	__isl_keep isl_ast_print_options *options, int in_block, int in_list);

static __isl_give isl_printer *isl_printer_print_ast_expr_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_expr *expr);

/* Print the body "node" of a for or if node.
 * If "else_node" is set, then it is printed as well.
 * If "force_block" is set, then print out the body as a block.
 * We first check if we need to print out a block.
 * We always print out a block if there is an else node to make
 * sure that the else node is matched to the correct if node.
 * For consistency, the corresponding else node is also printed as a block.
 *
 * If the else node is itself an if, then we print it as
 *
 *	} else if (..) {
 *	}
 *
 * Otherwise the else node is printed as
 *
 *	} else {
 *	  node
 *	}
 */
static __isl_give isl_printer *print_body_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_node *node, __isl_keep isl_ast_node *else_node,
	__isl_keep isl_ast_print_options *options, int force_block)
{
	if (!node)
		return isl_printer_free(p);

	if (!force_block && !else_node && !need_block(node)) {
		p = isl_printer_end_line(p);
		p = isl_printer_indent(p, 2);
                // TODO
                {
                    isl_ast_print_options * opt = isl_ast_print_options_copy(options);
                    if (!options || !node)
                        goto error;
                    p = print_ast_node_physl(p, node, options, 0, 0);
                    isl_ast_print_options_free(options);
                    return p;

error:
                    isl_ast_print_options_free(options);
                    isl_printer_free(p);
                    return nullptr;
                }
		//p = isl_ast_node_print(node, p,
		//			isl_ast_print_options_copy(options));
		p = isl_printer_indent(p, -2);
		return p;
	}

	p = isl_printer_print_str(p, " block( ");
	p = isl_printer_end_line(p);
	p = isl_printer_indent(p, 2);
	p = print_ast_node_physl(p, node, options, 1, 0);
	p = isl_printer_indent(p, -2);
	p = isl_printer_start_line(p);
	p = isl_printer_print_str(p, " ) ");
	if (else_node) {
                // ct note: this commented out section provides 
                //          support for 'else if' expressions 
                //
		//if (else_node->type == isl_ast_node_if) {
		//	p = isl_printer_print_str(p, " else ");
		//	p = print_if_physl(p, else_node, options, 0, 1);
                //
                // ct note: this section provides support for
                //          'else' expressions
		//} else {
			p = isl_printer_print_str(p, " , ");
			p = print_body_physl(p, else_node, NULL, options, 1);
	                p = isl_printer_print_str(p, " ) ");
		//}
	} else
		p = isl_printer_end_line(p);

	return p;
}

static __isl_give isl_printer *print_for_physl(
    __isl_take isl_printer *p,
    __isl_keep isl_ast_node *node,
    __isl_keep isl_ast_print_options *options, int in_block, int in_list)
{
	isl_id *id;
	const char *name;
	const char *type;

	type = isl_options_get_ast_iterator_type(isl_printer_get_ctx(p));
	if (!node->u.f.degenerate) {
		id = isl_ast_expr_get_id(node->u.f.iterator);
		name = isl_id_get_name(id);
		isl_id_free(id);
		p = isl_printer_start_line(p);
		p = isl_printer_print_str(p, "for( ");
		p = isl_printer_print_str(p, " store( ");
		p = isl_printer_print_str(p, name);
		p = isl_printer_print_str(p, ", ");
		p = isl_printer_print_ast_expr_physl(p, node->u.f.init);
		p = isl_printer_print_str(p, " ), ");
		p = isl_printer_print_ast_expr_physl(p, node->u.f.cond);
		p = isl_printer_print_str(p, ", ");
		p = isl_printer_print_str(p, " store( ");
		p = isl_printer_print_str(p, name);
		p = isl_printer_print_str(p, " , ");
		p = isl_printer_print_str(p, name);
		p = isl_printer_print_str(p, " + ");
		p = isl_printer_print_ast_expr_physl(p, node->u.f.inc);
		p = isl_printer_print_str(p, "), ");
		p = isl_printer_print_str(p, " block( ");
		p = print_body_physl(p, node->u.f.body, NULL, options, 0);
		p = isl_printer_print_str(p, " )"); // end block
		p = isl_printer_print_str(p, " )"); // end for
	} else {
		id = isl_ast_expr_get_id(node->u.f.iterator);
		name = isl_id_get_name(id);
		isl_id_free(id);
		if (!in_block || in_list)
			p = start_block(p);
		p = isl_printer_start_line(p);
		p = isl_printer_print_str(p, "store( ");
		p = isl_printer_print_str(p, name);
		p = isl_printer_print_str(p, " , ");
		p = isl_printer_print_ast_expr_physl(p, node->u.f.init);
		p = isl_printer_print_str(p, ")");
		p = isl_printer_end_line(p);
		p = print_ast_node_physl(p, node->u.f.body, options, 1, 0);
		if (!in_block || in_list)
			p = end_block(p);
	}

	return p;
}

/* Print the if node "node".
 * If "new_line" is set then the if node should be printed on a new line.
 * If "force_block" is set, then print out the body as a block.
 */
static __isl_give isl_printer *print_if_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_node *node,
	__isl_keep isl_ast_print_options *options, int new_line,
	int force_block)
{
	if (new_line)
		p = isl_printer_start_line(p);
	p = isl_printer_print_str(p, "if (");
	p = isl_printer_print_ast_expr_physl(p, node->u.i.guard);
	p = isl_printer_print_str(p, " , ");
	p = print_body_physl(p, node->u.i.then, node->u.i.else_node, options,
			force_block);
	p = isl_printer_print_str(p, " )");

	return p;
}

/* Return a string containing PhySL code representing this isl_ast_node.
__isl_give char *isl_ast_node_to_physl_str(__isl_keep isl_ast_node *node)
{
	isl_printer *p;
	char *str;

	if (!node)
	    return nullptr;

	p = isl_printer_to_str(isl_ast_node_get_ctx(node));
	p = isl_printer_print_ast_node(p, node);

	str = isl_printer_get_str(p);

	isl_printer_free(p);

	return str;
}
 */


/* Print a function call "expr" in C format.
 *
 * The first argument represents the function to be called.
 */
static __isl_give isl_printer *print_call_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_expr *expr)
{
	int i = 0;

	p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[0]);
	p = isl_printer_print_str(p, "(");
	for (i = 1; i < expr->u.op.n_arg; ++i) {
		if (i != 1)
			p = isl_printer_print_str(p, ", ");
		p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[i]);
	}
	p = isl_printer_print_str(p, ")");

	return p;
}

/* Print an array access "expr" in C format.
 *
 * The first argument represents the array being accessed.
 */
static __isl_give isl_printer *print_access_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_expr *expr)
{
	int i = 0;

	p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[0]);
	for (i = 1; i < expr->u.op.n_arg; ++i) {
		p = isl_printer_print_str(p, "[");
		p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[i]);
		p = isl_printer_print_str(p, "]");
	}

	return p;
}

/* Textual C representation of the various operators.
 */
static std::string op_str_c [] = {
	[isl_ast_op_and] = "&&",
	[isl_ast_op_and_then] = "&&",
	[isl_ast_op_or] = "||",
	[isl_ast_op_or_else] = "||",
	[isl_ast_op_max] = "max",
	[isl_ast_op_min] = "min",
	[isl_ast_op_minus] = "-",
	[isl_ast_op_add] = "+",
	[isl_ast_op_sub] = "-",
	[isl_ast_op_mul] = "*",
	[isl_ast_op_fdiv_q] = "floord",
	[isl_ast_op_pdiv_q] = "/",
	[isl_ast_op_pdiv_r] = "%",
	[isl_ast_op_zdiv_r] = "%",
	[isl_ast_op_div] = "/",
	[isl_ast_op_eq] = "==",
	[isl_ast_op_le] = "<=",
	[isl_ast_op_ge] = ">=",
	[isl_ast_op_lt] = "<",
	[isl_ast_op_gt] = ">",
	[isl_ast_op_member] = ".",
	[isl_ast_op_address_of] = "&"
};

/* Precedence in C of the various operators.
 * Based on http://en.wikipedia.org/wiki/Operators_in_C_and_C++
 * Lowest value means highest precedence.
 */
static int op_prec[] = {
	[isl_ast_op_and] = 13,
	[isl_ast_op_and_then] = 13,
	[isl_ast_op_or] = 14,
	[isl_ast_op_or_else] = 14,
	[isl_ast_op_max] = 2,
	[isl_ast_op_min] = 2,
	[isl_ast_op_minus] = 3,
	[isl_ast_op_add] = 6,
	[isl_ast_op_sub] = 6,
	[isl_ast_op_mul] = 5,
	[isl_ast_op_div] = 5,
	[isl_ast_op_fdiv_q] = 2,
	[isl_ast_op_pdiv_q] = 5,
	[isl_ast_op_pdiv_r] = 5,
	[isl_ast_op_zdiv_r] = 5,
	[isl_ast_op_cond] = 15,
	[isl_ast_op_select] = 15,
	[isl_ast_op_eq] = 9,
	[isl_ast_op_le] = 8,
	[isl_ast_op_ge] = 8,
	[isl_ast_op_lt] = 8,
	[isl_ast_op_gt] = 8,
	[isl_ast_op_call] = 2,
	[isl_ast_op_access] = 2,
	[isl_ast_op_member] = 2,
	[isl_ast_op_address_of] = 3
};

/* Is the operator left-to-right associative?
 */
static int op_left[] = {
	[isl_ast_op_and] = 1,
	[isl_ast_op_and_then] = 1,
	[isl_ast_op_or] = 1,
	[isl_ast_op_or_else] = 1,
	[isl_ast_op_max] = 1,
	[isl_ast_op_min] = 1,
	[isl_ast_op_minus] = 0,
	[isl_ast_op_add] = 1,
	[isl_ast_op_sub] = 1,
	[isl_ast_op_mul] = 1,
	[isl_ast_op_div] = 1,
	[isl_ast_op_fdiv_q] = 1,
	[isl_ast_op_pdiv_q] = 1,
	[isl_ast_op_pdiv_r] = 1,
	[isl_ast_op_zdiv_r] = 1,
	[isl_ast_op_cond] = 0,
	[isl_ast_op_select] = 0,
	[isl_ast_op_eq] = 1,
	[isl_ast_op_le] = 1,
	[isl_ast_op_ge] = 1,
	[isl_ast_op_lt] = 1,
	[isl_ast_op_gt] = 1,
	[isl_ast_op_call] = 1,
	[isl_ast_op_access] = 1,
	[isl_ast_op_member] = 1,
	[isl_ast_op_address_of] = 0
};

static int is_and(enum isl_ast_op_type op)
{
	return op == isl_ast_op_and || op == isl_ast_op_and_then;
}

static int is_or(enum isl_ast_op_type op)
{
	return op == isl_ast_op_or || op == isl_ast_op_or_else;
}

static int is_add_sub(enum isl_ast_op_type op)
{
	return op == isl_ast_op_add || op == isl_ast_op_sub;
}

static int is_div_mod(enum isl_ast_op_type op)
{
	return op == isl_ast_op_div ||
	       op == isl_ast_op_pdiv_r ||
	       op == isl_ast_op_zdiv_r;
}

/* Do we need/want parentheses around "expr" as a subexpression of
 * an "op" operation?  If "left" is set, then "expr" is the left-most
 * operand.
 *
 * We only need parentheses if "expr" represents an operation.
 *
 * If op has a higher precedence than expr->u.op.op, then we need
 * parentheses.
 * If op and expr->u.op.op have the same precedence, but the operations
 * are performed in an order that is different from the associativity,
 * then we need parentheses.
 *
 * An and inside an or technically does not require parentheses,
 * but some compilers complain about that, so we add them anyway.
 *
 * Computations such as "a / b * c" and "a % b + c" can be somewhat
 * difficult to read, so we add parentheses for those as well.
 */
static int sub_expr_need_parens(enum isl_ast_op_type op,
	__isl_keep isl_ast_expr *expr, int left)
{
	if (expr->type != isl_ast_expr_op)
		return 0;

	if (op_prec[expr->u.op.op] > op_prec[op])
		return 1;
	if (op_prec[expr->u.op.op] == op_prec[op] && left != op_left[op])
		return 1;

	if (is_or(op) && is_and(expr->u.op.op))
		return 1;
	if (op == isl_ast_op_mul && expr->u.op.op != isl_ast_op_mul &&
	    op_prec[expr->u.op.op] == op_prec[op])
		return 1;
	if (is_add_sub(op) && is_div_mod(expr->u.op.op))
		return 1;

	return 0;
}

/* Print "expr" as a subexpression of an "op" operation in C format.
 * If "left" is set, then "expr" is the left-most operand.
 */
static __isl_give isl_printer *print_sub_expr_physl(__isl_take isl_printer *p,
	enum isl_ast_op_type op, __isl_keep isl_ast_expr *expr, int left)
{
	int need_parens;

	need_parens = sub_expr_need_parens(op, expr, left);

	if (need_parens)
		p = isl_printer_print_str(p, "(");
	p = isl_printer_print_ast_expr_physl(p, expr);
	if (need_parens)
		p = isl_printer_print_str(p, ")");
	return p;
}

/* Return the textual representation of "type" in C format.
 *
 * If there is a user-specified name in an isl_ast_op_names note
 * associated to "p", then return that.
 * Otherwise, return the default name in op_str_c.
 */
static const char *get_op_str_physl(__isl_keep isl_printer *p,
	enum isl_ast_op_type type)
{
	isl_id *id;
	isl_bool has_names;
	struct isl_ast_op_names *names = NULL;

	id = names_id(isl_printer_get_ctx(p));
	has_names = isl_printer_has_note(p, id);
	if (has_names >= 0 && has_names)
		names = static_cast<struct isl_ast_op_names *>(get_note(p, id));
	isl_id_free(id);
	if (names && names->op_str[type])
		return names->op_str[type];
	return op_str_c[type].c_str();
}

/* Print a min or max reduction "expr" in C format.
 */
static __isl_give isl_printer *print_min_max_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_expr *expr)
{
	int i = 0;

	for (i = 1; i < expr->u.op.n_arg; ++i) {
		p = isl_printer_print_str(p, get_op_str_physl(p, expr->u.op.op));
		p = isl_printer_print_str(p, "(");
	}
	p = isl_printer_print_ast_expr(p, expr->u.op.args[0]);
	for (i = 1; i < expr->u.op.n_arg; ++i) {
		p = isl_printer_print_str(p, ", ");
		p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[i]);
		p = isl_printer_print_str(p, ")");
	}

	return p;
}

static __isl_give isl_printer *isl_printer_print_ast_expr_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_expr *expr)
{
	if (!p)
		return NULL;
	if (!expr)
		return isl_printer_free(p);

	switch (expr->type) {
	case isl_ast_expr_op:
		if (expr->u.op.op == isl_ast_op_call) {
			p = print_call_physl(p, expr);
			break;
		}
		if (expr->u.op.op == isl_ast_op_access) {
			p = print_access_physl(p, expr);
			break;
		}
		if (expr->u.op.n_arg == 1) {
			p = isl_printer_print_str(p,
						get_op_str_physl(p, expr->u.op.op));
			p = print_sub_expr_physl(p, expr->u.op.op,
						expr->u.op.args[0], 0);
			break;
		}
		if (expr->u.op.op == isl_ast_op_fdiv_q) {
			const char *name;

			name = get_op_str_physl(p, isl_ast_op_fdiv_q);
			p = isl_printer_print_str(p, name);
			p = isl_printer_print_str(p, "(");
			p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[0]);
			p = isl_printer_print_str(p, ", ");
			p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[1]);
			p = isl_printer_print_str(p, ")");
			break;
		}
		if (expr->u.op.op == isl_ast_op_max ||
		    expr->u.op.op == isl_ast_op_min) {
			p = print_min_max_physl(p, expr);
			break;
		}
		if (expr->u.op.op == isl_ast_op_cond ||
		    expr->u.op.op == isl_ast_op_select) {
			p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[0]);
			p = isl_printer_print_str(p, " ? ");
			p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[1]);
			p = isl_printer_print_str(p, " : ");
			p = isl_printer_print_ast_expr_physl(p, expr->u.op.args[2]);
			break;
		}
		if (expr->u.op.n_arg != 2)
			isl_die(isl_printer_get_ctx(p), isl_error_internal,
				"operation should have two arguments",
				return isl_printer_free(p));
		p = print_sub_expr_physl(p, expr->u.op.op, expr->u.op.args[0], 1);
		if (expr->u.op.op != isl_ast_op_member)
			p = isl_printer_print_str(p, " ");
		p = isl_printer_print_str(p, get_op_str_physl(p, expr->u.op.op));
		if (expr->u.op.op != isl_ast_op_member)
			p = isl_printer_print_str(p, " ");
		p = print_sub_expr_physl(p, expr->u.op.op, expr->u.op.args[1], 0);
		break;
	case isl_ast_expr_id:
		p = isl_printer_print_str(p, isl_id_get_name(expr->u.id));
		break;
	case isl_ast_expr_int:
		p = isl_printer_print_val(p, expr->u.v);
		break;
	case isl_ast_expr_error:
		break;
	}

	return p;
}

/* Print the "node" to "p".
 *
 * "in_block" is set if we are currently inside a block.
 * If so, we do not print a block around the children of a block node.
 * We do this to avoid an extra block around the body of a degenerate
 * for node.
 *
 * "in_list" is set if the current node is not alone in the block.
 */
static __isl_give isl_printer *print_ast_node_physl(__isl_take isl_printer *p,
	__isl_keep isl_ast_node *node,
	__isl_keep isl_ast_print_options *options, int in_block, int in_list)
{
	switch (node->type) {
	case isl_ast_node_for:
		if (options->print_for) {
			return options->print_for(p,
					isl_ast_print_options_copy(options),
					node, options->print_for_user);
                }
		p = print_for_physl(p, node, options, in_block, in_list);
		break;
	case isl_ast_node_if:
		p = print_if_physl(p, node, options, 1, 0);
		break;
	case isl_ast_node_block:
		if (!in_block)
			p = start_block(p);
		p = isl_ast_node_list_print__(node->u.b.children, p, options);
		if (!in_block)
			p = end_block(p);
		break;
	case isl_ast_node_mark:
		p = isl_printer_start_line(p);
		p = isl_printer_print_str(p, "// ");
		p = isl_printer_print_str(p, isl_id_get_name(node->u.m.mark));
		p = isl_printer_end_line(p);
		p = print_ast_node_physl(p, node->u.m.node, options, 0, in_list);
		break;
	case isl_ast_node_user:
		if (options->print_user) {
			return options->print_user(p,
					isl_ast_print_options_copy(options),
					node, options->print_user_user);
                }
		p = isl_printer_start_line(p);
		p = isl_printer_print_ast_expr_physl(p, node->u.e.expr);
		//p = isl_printer_print_str(p, ")");
		p = isl_printer_end_line(p);
		break;
	case isl_ast_node_error:
		break;
	}
	return p;
}

static __isl_give char *isl_ast_node_to_physl_str(isl_ctx* ctx, isl_ast_node* node)
{
	isl_printer *p = nullptr;
	char *str = nullptr;

	if (!node) {
	    return nullptr;
        }

	p = isl_printer_to_str(ctx); //isl_ast_node_get_ctx(node));

        isl_ast_print_options *options = isl_ast_print_options_alloc(isl_printer_get_ctx(p));
	p = print_ast_node_physl(p, node, options, 0, 0);
	str = isl_printer_get_str(p);

        isl_ast_print_options_free(options);
	isl_printer_free(p);

	return str;
}

__isl_give isl_printer *isl_ast_node_list_print__(
        __isl_keep isl_ast_node_list *list, __isl_take isl_printer *p,
        __isl_keep isl_ast_print_options *options)
{
        int i;

        if (!p || !list || !options)
                return isl_printer_free(p);

        for (i = 0; i < list->n; ++i)
                p = print_ast_node_physl(p, list->p[i], options, 1, 1);

        return p;
}

struct physl_codegen {

static inline std::string bin_op(const std::string & op, const std::string & x, const std::string & y) {
    return op + "(" + x + ", " + y + ")";
}

static inline std::string uni_op(const std::string & op, const std::string & x) {
    return op + "(" + x + ")";
}


static inline std::string bin_expr(const std::string & op, const std::string & x, const std::string & y) {
    return x + " " + op + " " + y;
}

static inline std::string uni_expr(const std::string & op, const std::string & x) {
    return op + " " + x;
}

static std::string and_(const std::string & x, const std::string & y) {
    return bin_op("and", x, y);
}

static std::string or_(const std::string & x, const std::string & y) {
    return bin_op("or", x, y);
}

static std::string max_(const std::string & x, const std::string & y) {
    return bin_op("max", x, y);
}

static std::string min_(const std::string & x, const std::string & y) {
    return bin_op("min", x, y);
}

static std::string minus_(const std::string & x) {
    return uni_expr("-", x);
}

static std::string add_(const std::string & x, const std::string & y) {
    return bin_expr("+", x, y);
}

static std::string sub_(const std::string & x, const std::string & y) {
    return bin_expr("-", x, y);
}

static std::string div_(const std::string & x, const std::string & y) {
    return bin_expr("/", x, y);
}

static std::string mul_(const std::string & x, const std::string & y) {
    return bin_expr("*", x, y);
}

static std::string mod_(const std::string & x, const std::string & y) {
    return bin_expr("%", x, y);
}

static std::string le_(const std::string & x, const std::string & y) {
    return bin_expr("<=", x, y);
}

static std::string lt_(const std::string & x, const std::string & y) {
    return bin_expr("<", x, y);
}

static std::string ge_(const std::string & x, const std::string & y) {
    return bin_expr(">=", x, y);
}

static std::string gt_(const std::string & x, const std::string & y) {
    return bin_expr(">", x, y);
}

static std::string not_(const std::string & x) {
    return uni_expr("!", x);
}

static std::string eq_(const std::string & x, const std::string & y) {
    return bin_expr("==", x, y);
}

static std::string ne_(const std::string & x, const std::string & y) {
    return bin_expr("!=", x, y);
}

static std::string rshift_(const std::string & x, const std::string & y) {
    return bin_expr(">>", x, y);
}

static std::string lshift_(const std::string & x, const std::string & y) {
    return bin_expr("<<", x, y);
}

static std::string floor_(const std::string & x) {
    return uni_op("floor", x);
}

static std::string sin_(const std::string & x) {
    return uni_op("sin", x);
}

static std::string cos_(const std::string & x) {
    return uni_op("cos", x);
}

static std::string tan_(const std::string & x) {
    return uni_op("tan", x);
}

static std::string asin_(const std::string & x) {
    return uni_op("asin", x);
}

static std::string acos_(const std::string & x) {
    return uni_op("acos", x);
}

static std::string atan_(const std::string & x) {
    return uni_op("atan", x);
}

static std::string sinh_(const std::string & x) {
    return uni_op("sinh", x);
}

static std::string cosh_(const std::string & x) {
    return uni_op("cosh", x);
}

static std::string tanh_(const std::string & x) {
    return uni_op("tanh", x);
}

static std::string asinh_(const std::string & x) {
    return uni_op("asinh", x);
}

static std::string acosh_(const std::string & x) {
    return uni_op("acosh", x);
}

static std::string atanh_(const std::string & x) {
    return uni_op("atanh", x);
}

static std::string exp_(const std::string & x) {
    return uni_op("exp", x);
}

static std::string log_(const std::string & x) {
    return uni_op("log", x);
}

static std::string ceil_(const std::string & x) {
    return uni_op("ceil", x);
}

static std::string abs_(const std::string & x) {
    return uni_op("abs", x);
}

static std::string sqrt_(const std::string & x) {
    return uni_op("sqrt", x);
}

static inline std::string var_(const std::string &name) { return name; }

static std::string call_(const std::string & name, std::vector<std::string> const & args) {

    std::string ret{};
    ret += name + "(";

    const std::int64_t args_size = args.size();
    for(std::int64_t i = 0; i < args_size; ++i) {
        ret += (i < (args_size-1)) ? (args[i] + ",") : args[i];
    }

    ret += ")";

    return ret;
}


}; // end class physl_codegen

// https://github.com/Tiramisu-Compiler/tiramisu/blob/62e1513d1580aa7ba304d3ebe22f631dfe30814d/src/tiramisu_codegen_halide.cpp
//
static void physl_from_tiramisu_expr(const ::tiramisu::expr & tiramisu_expr, std::string & ret_result) {

    if (tiramisu_expr.get_expr_type() == ::tiramisu::e_val)
    {
        if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint8)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_uint8_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int8)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_int8_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint16)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_uint16_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int16)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_int16_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint32)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_uint32_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int32)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_int32_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint64)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_uint64_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int64)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_int64_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_float32)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_float32_value()));
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_float64)
        {
            ret_result.append(std::to_string(tiramisu_expr.get_float64_value()));
        }
    }
    else if (tiramisu_expr.get_expr_type() == tiramisu::e_op)
    {
        //Halide::Expr op0, op1, op2;
        std::string op0{}, op1{}, op2{};

        DEBUG(10, tiramisu::str_dump("tiramisu expression of type tiramisu::e_op"));

        if (tiramisu_expr.get_n_arg() > 0)
        {
            tiramisu::expr expr0 = tiramisu_expr.get_operand(0);
            //op0
            physl_from_tiramisu_expr(expr0, op0); //comp);
        }

        if (tiramisu_expr.get_n_arg() > 1)
        {
            tiramisu::expr expr1 = tiramisu_expr.get_operand(1);
            //op1
            physl_from_tiramisu_expr(expr1, op1); //, comp);
        }

        if (tiramisu_expr.get_n_arg() > 2)
        {
            tiramisu::expr expr2 = tiramisu_expr.get_operand(2);
            //op2
            physl_from_tiramisu_expr(expr2, op2); //, comp);
        }

        switch (tiramisu_expr.get_op_type())
        {
            case tiramisu::o_logical_and:
                ret_result.append( physl_codegen::and_(op0, op1) );
                DEBUG(10, tiramisu::str_dump("op type: o_logical_and"));
                break;
            case tiramisu::o_logical_or:
                ret_result.append(physl_codegen::or_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_logical_or"));
                break;
            case tiramisu::o_max:
                ret_result.append(physl_codegen::max_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_max"));
                break;
            case tiramisu::o_min:
                ret_result.append(physl_codegen::min_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_min"));
                break;
            case tiramisu::o_minus:
                ret_result.append(physl_codegen::minus_(op0)); //, true);
                DEBUG(10, tiramisu::str_dump("op type: o_minus"));
                break;
            case tiramisu::o_add:
                ret_result.append(physl_codegen::add_(op0, op1)); //, true);
                DEBUG(10, tiramisu::str_dump("op type: o_add"));
                break;
            case tiramisu::o_sub:
                ret_result.append(physl_codegen::sub_(op0, op1)); //, true);
                DEBUG(10, tiramisu::str_dump("op type: o_sub"));
                break;
            case tiramisu::o_mul:
                ret_result.append(physl_codegen::mul_(op0, op1)); //, true);
                DEBUG(10, tiramisu::str_dump("op type: o_mul"));
                break;
            case tiramisu::o_div:
                ret_result.append(physl_codegen::div_(op0, op1)); //, true);
                DEBUG(10, tiramisu::str_dump("op type: o_div"));
                break;
            case tiramisu::o_mod:
                ret_result.append(physl_codegen::mod_(op0, op1)); //, true);
                DEBUG(10, tiramisu::str_dump("op type: o_mod"));
                break;
/*
            case tiramisu::o_select:
                result = Halide::Internal::Select::make(op0, op1, op2);
                DEBUG(10, tiramisu::str_dump("op type: o_select"));
                break;
            case tiramisu::o_lerp:
                result = Halide::lerp(op0, op1, op2);
                DEBUG(10, tiramisu::str_dump("op type: lerp"));
                break;
            case tiramisu::o_cond:
                ERROR("Code generation for o_cond is not supported yet.", true);
                break;
*/
            case tiramisu::o_le:
                ret_result.append(physl_codegen::le_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_le"));
                break;
            case tiramisu::o_lt:
                ret_result.append(physl_codegen::lt_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_lt"));
                break;
            case tiramisu::o_ge:
                ret_result.append(physl_codegen::ge_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_ge"));
                break;
            case tiramisu::o_gt:
                ret_result.append(physl_codegen::gt_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_gt"));
                break;
            case tiramisu::o_logical_not:
                ret_result.append(physl_codegen::not_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_not"));
                break;
            case tiramisu::o_eq:
                ret_result.append(physl_codegen::eq_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_eq"));
                break;
            case tiramisu::o_ne:
                ret_result.append(physl_codegen::ne_(op0, op1));
                DEBUG(10, tiramisu::str_dump("op type: o_ne"));
                break;
/*
            case tiramisu::o_type:
                result = halide_expr_from_tiramisu_type(tiramisu_expr.get_data_type());
                break;
*/
            case tiramisu::o_access:
            case tiramisu::o_lin_index:
            case tiramisu::o_address:
            case tiramisu::o_address_of:
            {

std::cout << "here" << std::endl;

                DEBUG(10, tiramisu::str_dump("op type: o_access or o_address"));
/*
                const char *access_comp_name = NULL;

                if (tiramisu_expr.get_op_type() == tiramisu::o_access ||
                    tiramisu_expr.get_op_type() == tiramisu::o_lin_index ||
                    tiramisu_expr.get_op_type() == tiramisu::o_address_of)
                {
                    access_comp_name = tiramisu_expr.get_name().c_str();
                }
                else if (tiramisu_expr.get_op_type() == tiramisu::o_address)
                {
                    access_comp_name = tiramisu_expr.get_operand(0).get_name().c_str();
                }
                else
                {
                    ERROR("Unsupported operation.", true);
                }

                assert(access_comp_name != NULL);

                DEBUG(10, tiramisu::str_dump("Computation being accessed: "); tiramisu::str_dump(access_comp_name));

                // Since we modify the names of update computations but do not modify the
                // expressions.  When accessing the expressions we find the old names, so
                // we need to look for the new names instead of the old names.
                // We do this instead of actually changing the expressions, because changing
                // the expressions will make the semantics of the printed program ambiguous,
                // since we do not have any way to distinguish between which update is the
                // consumer is consuming exactly.
                std::vector<tiramisu::computation *> computations_vector
                        = fct->get_computation_by_name(access_comp_name);
                if (computations_vector.size() == 0)
                {
                    // Search for update computations.
                    computations_vector
                            = fct->get_computation_by_name("_" + std::string(access_comp_name) + "_update_0");
                    assert((computations_vector.size() > 0) && "Computation not found.");
                }

                // We assume that computations that have the same name write all to the same buffer
                // but may have different access relations.
                tiramisu::computation *access_comp = computations_vector[0];
                assert((access_comp != NULL) && "Accessed computation is NULL.");
                if (comp && comp->is_wait()) {
                    // swap
                    // use operations_vector[0] instead of access_comp because we need it to be non-const
                    isl_map *orig = computations_vector[0]->get_access_relation();
                    computations_vector[0]->set_access(computations_vector[0]->wait_access_map);
                    computations_vector[0]->wait_access_map = orig;
                }
                isl_map *acc = access_comp->get_access_relation_adapted_to_time_processor_domain();
                if (comp && comp->is_wait()) {
                    // swap back
                    isl_map *orig = computations_vector[0]->get_access_relation();
                    computations_vector[0]->set_access(computations_vector[0]->wait_access_map);
                    computations_vector[0]->wait_access_map = orig;
                }
                const char *buffer_name = isl_space_get_tuple_name(
                        isl_map_get_space(acc),
                        isl_dim_out);
                assert(buffer_name != NULL);
                DEBUG(10, tiramisu::str_dump("Name of the associated buffer: "); tiramisu::str_dump(buffer_name));

                const auto &buffer_entry = fct->get_buffers().find(buffer_name);
                assert(buffer_entry != fct->get_buffers().end());

                const auto &tiramisu_buffer = buffer_entry->second;
//mod
                Halide::Type type = halide_type_from_tiramisu_type(tiramisu_buffer->get_elements_type());

                // Tiramisu buffer is from outermost to innermost, whereas Halide buffer is from innermost
                // to outermost; thus, we need to reverse the order
//mod
                halide_dimension_t *shape = new halide_dimension_t[tiramisu_buffer->get_dim_sizes().size()];
                int stride = 1;
//mod
                std::vector<Halide::Expr> strides_vector;
                //std::vector<std::string> strides_vector;

                if (tiramisu_buffer->has_constant_extents())
                {
                    DEBUG(10, tiramisu::str_dump("Buffer has constant extents."));
                    for (size_t i = 0; i < tiramisu_buffer->get_dim_sizes().size(); i++)
                    {
                        shape[i].min = 0;
                        int dim_idx = tiramisu_buffer->get_dim_sizes().size() - i - 1;
                        shape[i].extent = (int)tiramisu_buffer->get_dim_sizes()[dim_idx].get_int_val();
                        shape[i].stride = stride;
                        stride *= (int)tiramisu_buffer->get_dim_sizes()[dim_idx].get_int_val();
                    }
                }
                else
                {
                    DEBUG(10, tiramisu::str_dump("Buffer has non-constant extents."));
                    std::vector<isl_ast_expr *> empty_index_expr;
//mod
                    //Halide::Expr stride_expr = Halide::Expr(1);
                    std::string stride_expr{"1"};
                    for (int i = 0; i < tiramisu_buffer->get_dim_sizes().size(); i++)
                    {
                        int dim_idx = tiramisu_buffer->get_dim_sizes().size() - i - 1;
                        strides_vector.push_back(stride_expr);
                        stride_expr = stride_expr * physl_from_tiramisu_expr(fct, empty_index_expr, tiramisu_buffer->get_dim_sizes()[dim_idx], comp);
                    }
                }
                DEBUG(10, tiramisu::str_dump("Buffer strides have been computed."));

                if (tiramisu_expr.get_op_type() == tiramisu::o_access ||
                    tiramisu_expr.get_op_type() == tiramisu::o_address_of ||
                    tiramisu_expr.get_op_type() == tiramisu::o_lin_index)
                {
                    Halide::Expr index;

                    // If index_expr is empty, and since tiramisu_expr is
                    // an access expression, this means that index_expr was not
                    // computed using the statement generator because this
                    // expression is not an expression that is associated with
                    // a computation. It is rather an expression used by
                    // a computation (for example, as the size of a buffer
                    // dimension). So in this case, we retrieve the indices directly
                    // from tiramisu_expr.
                    // The possible problem in this case, is that the indices
                    // in tiramisu_expr cannot be adapted to the schedule if
                    // these indices are i, j, .... This means that these
                    // indices have to be constant value only. So we check for this.
                    if (index_expr.size() == 0)
                    {
                        DEBUG(10, tiramisu::str_dump("index_expr is empty. Retrieving access indices directly from the tiramisu access expression without scheduling."));

                        for (int i = 0; i < tiramisu_buffer->get_dim_sizes().size(); i++)
                        {
			    // Actually any computation access that does not require
			    // scheduling is supported.
			    // Other access that require scheduling should not
			    // be accepted since we do not schedule them.
			    // Currently we allow all accesses since we do not have
			    // a way to check if an iterator is requires scheduling
			    // or not. But we show a warning if the access is
			    // not constant.
			    if (tiramisu_expr.get_access()[i].is_constant() == false)
			    {
				DEBUG(3, tiramisu::str_dump("Possible error in code generation because the non-affine access."));
				DEBUG(3, tiramisu::str_dump("Currently we do not schedule those accesses, but we allow them,"));
				DEBUG(3, tiramisu::str_dump("therefore they might cause a problem in code generation."));

			    }
                            // assert(tiramisu_expr.get_access()[i].is_constant() && "Only constant accesses are supported.");
                        }

                        if (tiramisu_buffer->has_constant_extents())
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), shape, tiramisu_expr.get_access());
                        else
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), strides_vector, tiramisu_expr.get_access());
                    }
                    else
                    {
                        DEBUG(10, tiramisu::str_dump("index_expr is NOT empty. Retrieving access indices from index_expr (i.e., retrieving indices adapted to the schedule)."));
                        if (tiramisu_buffer->has_constant_extents())
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), shape, index_expr[0]);
                        else
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), strides_vector, index_expr[0]);

                        index_expr.erase(index_expr.begin());
                    }
                    if (tiramisu_expr.get_op_type() == tiramisu::o_lin_index) {
                        result = index;
                    }
//mod
                    else if (tiramisu_buffer->get_argument_type() == tiramisu::a_input)
                    {
                        //Halide::Buffer<> buffer = Halide::Buffer<>(
                        //                              type,
                        //                              tiramisu_buffer->get_data(),
                        //                              tiramisu_buffer->get_dim_sizes().size(),
                        //                              shape,
                        //                              tiramisu_buffer->get_name());

                        Halide::Internal::Parameter param =
                                Halide::Internal::Parameter(halide_type_from_tiramisu_type(tiramisu_buffer->get_elements_type()),
                                                            true,
                                                            tiramisu_buffer->get_dim_sizes().size(),
                                                            tiramisu_buffer->get_name());

                        // TODO(psuriana): ImageParam is not currently supported.
                        if (tiramisu_expr.get_op_type() != tiramisu::o_address_of) {
                            result = Halide::Internal::Load::make(
                                    type, tiramisu_buffer->get_name(), index, Halide::Buffer<>(),
                                    param, Halide::Internal::const_true(type.lanes()));
                        } else {
                            result = Halide::Internal::Variable::make(Halide::type_of<struct halide_buffer_t *>(),
                                                                                   tiramisu_buffer->get_name() + ".buffer");
                            result = Halide::Internal::Call::make(Halide::Handle(1, type.handle_type),
                                                                  "tiramisu_address_of_" +
                                                                  str_from_tiramisu_type_primitive(tiramisu_buffer->get_elements_type()),
                                                                  {result, index},
                                                                  Halide::Internal::Call::Extern);
                        }
                    }
                    else
                    {
                        if (tiramisu_expr.get_op_type() != tiramisu ::o_address_of) {
                            result = Halide::Internal::Load::make(
                                    type, tiramisu_buffer->get_name(), index, Halide::Buffer<>(),
                                    Halide::Internal::Parameter(), Halide::Internal::const_true(type.lanes()));
                        } else {
                            result = Halide::Internal::Variable::make(Halide::type_of<struct halide_buffer_t *>(),
                                                                      tiramisu_buffer->get_name() + ".buffer");
                            result = Halide::Internal::Call::make(Halide::Handle(1, type.handle_type),
                                                                  "tiramisu_address_of_" +
                                                                  str_from_tiramisu_type_primitive(tiramisu_buffer->get_elements_type()),
                                                                  {result, index},
                                                                  Halide::Internal::Call::Extern);
                        }
                    }
                }
                else if (tiramisu_expr.get_op_type() == tiramisu::o_address)
                {
                    // Create a pointer to Halide buffer.
                    result = Halide::Internal::Variable::make(Halide::type_of<struct halide_buffer_t *>(),
                                                              tiramisu_buffer->get_name() + ".buffer");
                }
                delete[] shape;
*/
            }
                break;
            case tiramisu::o_right_shift:
                ret_result.append(physl_codegen::rshift_( op0 , op1 ));
                DEBUG(10, tiramisu::str_dump("op type: o_right_shift"));
                break;
            case tiramisu::o_left_shift:
                ret_result.append(physl_codegen::lshift_( op0 , op1 ));
                DEBUG(10, tiramisu::str_dump("op type: o_left_shift"));
                break;
            case tiramisu::o_floor:
                ret_result.append(physl_codegen::floor_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_floor"));
                break;
/*
            case tiramisu::o_cast:
                result = Halide::cast(halide_type_from_tiramisu_type(tiramisu_expr.get_data_type()), op0);
                DEBUG(10, tiramisu::str_dump("op type: o_cast"));
                break;
*/
            case tiramisu::o_sin:
                ret_result.append(physl_codegen::sin_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_sin"));
                break;
            case tiramisu::o_cos:
                ret_result.append( physl_codegen::cos_(op0)); 
                DEBUG(10, tiramisu::str_dump("op type: o_cos"));
                break;
            case tiramisu::o_tan:
                ret_result.append(physl_codegen::tan_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_tan"));
                break;
            case tiramisu::o_asin:
                ret_result.append(physl_codegen::asin_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_asin"));
                break;
            case tiramisu::o_acos:
                ret_result.append(physl_codegen::acos_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_acos"));
                break;
            case tiramisu::o_atan:
                ret_result.append(physl_codegen::atan_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_atan"));
                break;
            case tiramisu::o_sinh:
                ret_result.append(physl_codegen::sinh_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_sinh"));
                break;
            case tiramisu::o_cosh:
                ret_result.append(physl_codegen::cosh_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_cosh"));
                break;
            case tiramisu::o_tanh:
                ret_result.append(physl_codegen::tanh_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_tanh"));
                break;
            case tiramisu::o_asinh:
                ret_result.append(physl_codegen::asinh_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_asinh"));
                break;
            case tiramisu::o_acosh:
                ret_result.append(physl_codegen::acosh_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_acosh"));
                break;
            case tiramisu::o_atanh:
                ret_result.append(physl_codegen::atanh_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_atanh"));
                break;
            case tiramisu::o_abs:
                ret_result.append(physl_codegen::abs_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_abs"));
                break;
            case tiramisu::o_sqrt:
                ret_result.append(physl_codegen::sqrt_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_sqrt"));
                break;
            case tiramisu::o_expo:
                ret_result.append(physl_codegen::exp_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_expo"));
                break;
            case tiramisu::o_log:
                ret_result.append(physl_codegen::log_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_log"));
                break;
            case tiramisu::o_ceil:
                ret_result.append(physl_codegen::ceil_(op0));
                DEBUG(10, tiramisu::str_dump("op type: o_ceil"));
                break;
/*
            case tiramisu::o_round:
                result = Halide::round(op0);
                DEBUG(10, tiramisu::str_dump("op type: o_round"));
                break;
            case tiramisu::o_trunc:
                result = Halide::trunc(op0);
                DEBUG(10, tiramisu::str_dump("op type: o_trunc"));
                break;
*/
            case tiramisu::o_call:
            {
                auto args = tiramisu_expr.get_arguments();
                std::vector<std::string> vec;
                vec.resize(args.size());

                std::transform(args.begin(), args.end(), vec.begin(),
                    [](auto & e) {
                    std::string res{};
                    physl_from_tiramisu_expr(e, res);
                    return res;
                });

                ret_result.append(physl_codegen::call_(tiramisu_expr.get_name(), vec));

/*
                for (const auto &e : tiramisu_expr.get_arguments())
                {
                    vec.push_back(he);
                }

                result = Halide::Internal::Call::make(halide_type_from_tiramisu_type(tiramisu_expr.get_data_type()),
                                                      tiramisu_expr.get_name(),
                                                      vec,
                                                      Halide::Internal::Call::CallType::Extern);
*/
                DEBUG(10, tiramisu::str_dump("op type: o_call"));
                break;
            }
/*
            case tiramisu::o_allocate:
            case tiramisu::o_free:
                ERROR("An expression of type o_allocate or o_free "
                                        "should not be passed to this function", true);
                break;
*/
            default:
                ERROR("Translating an unsupported ISL expression into a Halide expression.", 1);
        }
    }
    else if (tiramisu_expr.get_expr_type() == tiramisu::e_var)
    {
        DEBUG(3, tiramisu::str_dump("Generating a variable access expression."));
        DEBUG(3, tiramisu::str_dump("Expression is a variable of type: " + tiramisu::str_from_tiramisu_type_primitive(tiramisu_expr.get_data_type())));
        ret_result.append(physl_codegen::var_(tiramisu_expr.get_name()));

        /* Halide::Internal::Variable::make(
                halide_type_from_tiramisu_type(tiramisu_expr.get_data_type()),
                tiramisu_expr.get_name());
        */
    }
/*
    else
    {
        tiramisu::str_dump("tiramisu type of expr: ",
                           str_from_tiramisu_type_expr(tiramisu_expr.get_expr_type()).c_str());
        ERROR("\nTranslating an unsupported ISL expression in a Halide expression.", 1);
    }

    if (result.defined())
    {
        DEBUG(10, tiramisu::str_dump("Generated stmt: "); std::cout << result);
    }
*/

    DEBUG_INDENT(-4);
    DEBUG_FCT_NAME(10);
}

int generate_physl(isl_ctx * ctx, isl_ast_node * node, const ::tiramisu::expr & e) {
    isl_printer *p = isl_printer_to_file(ctx, stdout); //isl_ast_node_get_ctx(node.get()), stdout);
    isl_ast_print_options *options = isl_ast_print_options_alloc(isl_printer_get_ctx(p));

    p = print_ast_node_physl(p, node, options, 0, 0);

    isl_ast_print_options_free(options);
    isl_printer_free(p);

    std::string str{};
    physl_from_tiramisu_expr(e, str);
    std::cout << str << std::endl;

    return 1;
}


int generate_physl(isl_ctx * ctx, isl_ast_node * node, const ::tiramisu::expr & e, const std::string kernel_str, std::ostream & fstr) {
    char *c_str = isl_ast_node_to_physl_str(ctx, node);
    std::string cstr{(c_str == nullptr) ? "" : c_str };
    fstr << cstr; //(cstr.c_str(), cstr.size());

    std::string str{};
    physl_from_tiramisu_expr(e, str);
    fstr << str;

    return 1;
}

int generate_physl(isl_ctx * ctx, isl_ast_node * node, const ::tiramisu::expr & e, const std::string& kernel_str, std::string & physlstr) {
    char * c_str = isl_ast_node_to_physl_str(ctx, node);
    std::string cstr{(c_str == nullptr) ? "" : c_str };

    std::string str{};
    physl_from_tiramisu_expr(e, str);
    physlstr.assign(cstr + str);

    return 1;
}

} /* end namespace codegen */ } // end namespace physl
