> 从gcc命令中抠出clang插件所需内容,由于gcc和clang的差异 比如 gcc某个选项没有对应的clang选项（很多选项有此情况）、自带的头文件路径(-include -isystem -I)不等价 导致clang插件命令要补头文件路径 但同一个类型或宏有多个头文件含有 没有足够知识确定应该用哪一个头文件、报错不等价 gcc正常时clang可能报错 不能肯定地知道应该如何修补此报错，由于这些问题 导致 gcc命令转为clang插件命令 实践中不可行，因此 否定clang插件 而 只能转向gcc插件 即 既然 gcc编译命令 能正常 那么 向 正常的gcc命令中  增加插件调用 应该也能正常。
> gcc插件编写思路：
-   1. gcc官方文档？估计一头雾水
-   2. 问chatgpt （比如 https://vip.easychat.work/#/） 问: gcc11插件 对每个函数开头增加一行内联汇编语句。 
>     其会给出完成一个gcc插件大致步骤和插件内容, 具体如下:

要在每个函数的开头增加一行内联汇编语句，可以使用 GCC 11 的插件机制来实现。以下是一个示例插件代码，它将在每个函数的开头插入一行内联汇编语句：

```c
#include <gcc-plugin.h>
#include <tree.h>
#include <plugin-version.h>
#include <context.h>
#include <function.h>
#include <tree-pass.h>
#include <tree-ssa-alias.h>
#include <diagnostic.h>

int plugin_is_GPL_compatible;

static struct plugin_info my_plugin_info = {
    .version = "1.0",
    .help = "Add inline assembly at the beginning of each function",
};

static void insert_inline_asm(void *gcc_data, void *user_data)
{
    if (DECL_FUNCTION_CODE(gcc_data) == FUNCTION_DECL)
    {
        tree function = (tree)gcc_data;
        tree body = DECL_SAVED_TREE(function);

        if (body && TREE_CODE(body) == BLOCK)
        {
            tree asm_stmt = build_asm_string_literal("asm(\"your_inline_asm_code\");");
            tree first_stmt = BLOCK_SUBBLOCKS(body);

            if (first_stmt)
            {
                tree new_stmt = build3(ASM_EXPR, void_type_node, asm_stmt, NULL, NULL);
                BLOCK_SUBBLOCKS(body) = tree_cons(NULL, new_stmt, first_stmt);
            }
        }
    }
}

static struct register_pass_info my_pass_info = {
    .type = PLUGIN_PASS_FUNCTION,
    .name = "insert_inline_asm",
    .optinfo_flags = OPTGROUP_NONE,
    .tv_id = TV_NONE,
    .properties_required = PROP_gimple_leh | PROP_cfg,
    .properties_provided = 0,
    .properties_destroyed = 0,
    .todo_flags_start = 0,
    .todo_flags_finish = 0,
    .function = insert_inline_asm,
    .priority = 1000,
};

int plugin_init(struct plugin_name_args *plugin_info, struct plugin_gcc_version *version)
{
    if (!plugin_default_version_check(version, &gcc_version))
    {
        error(G_("incompatible gcc/plugin versions"));
        return 1;
    }

    register_callback(plugin_info->base_name, PLUGIN_INFO, NULL, &my_plugin_info);
    register_callback(plugin_info->base_name, PLUGIN_PASS_MANAGER_SETUP, NULL, &my_pass_info);

    return 0;
}
```

请注意，上述代码是一个简化的示例，仅用于说明插件机制的基本原理。您需要根据自己的需求进行修改和扩展。

要使用该插件，您需要按照以下步骤进行编译和安装：

1. 将上述代码保存为 `insert_inline_asm.c` 文件。
2. 使用以下命令编译插件：

   ```shell
   gcc -shared -o insert_inline_asm.so -fPIC insert_inline_asm.c -I /path/to/gcc/include
   ```

   其中，`/path/to/gcc/include` 是您的 GCC 安装目录中的 `include` 文件夹路径。请根据您的实际情况进行替换。
   
3. 将生成的 `insert_inline_asm.so` 插件文件复制到合适的目录，例如 `/usr/lib/gcc/x86_64-linux-gnu/{version}/plugin/`。

完成上述步骤后，插件将被加载并在编译时自动将内联汇编语句插入每个函数的开头。

请注意，使用插件时要小心，确保您的内联汇编语句是正确且安全的。不正确的使用内联汇编可能导致程序崩溃或产生不可预测的行为。建议在使用插件之前进行充分的测试和验证。
