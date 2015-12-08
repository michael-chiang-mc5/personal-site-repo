from django.template import Library
register = Library()

# returns True if post_tree_element is indent
@register.filter
def is_indent( post_tree_element ):
    indent_prefix = 'in-'
    if type(post_tree_element) is not str:
        return False
    elif post_tree_element.startswith(indent_prefix):
        return True
    else:
        return False

# returns True if post_tree_element is dedent
@register.filter
def is_dedent( post_tree_element ):
    dedent_prefix = 'out-'
    if type(post_tree_element) is not str:
        return False
    elif post_tree_element.startswith(dedent_prefix):
        return True
    else:
        return False

@register.filter
def get_dent_node_depth( text ):
    indent_prefix = 'in-'
    dedent_prefix = 'out-'
    if text.startswith(indent_prefix):
        depth = int(text[len(indent_prefix):])
    elif text.startswith(dedent_prefix):
        depth = int(text[len(dedent_prefix):])
    return depth

# Usage (in template):
# {{ post|post_upvoted_by_user:user_pk }}
#
# Results with the HTML:
# True
@register.filter
def post_upvoted_by_user(post,user_pk):
    return post.upvoters.filter(id=user_pk).exists()

# Usage (in template):
# {{ post|post_downvoted_by_user:user_pk }}
# Results with the HTML:
# True
@register.filter
def post_downvoted_by_user(post,user_pk):
    return post.downvoters.filter(id=user_pk).exists()
