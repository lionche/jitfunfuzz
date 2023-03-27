// 导入 esprima 库
const esprima = require('esprima');
const estraverse = require('estraverse');
const escodegen = require('escodegen');
//引入commander
const commander = require("commander");

const fs = require("fs");

let filename = '';

//增加命令行选项（-f 输入文件）
commander
    .option('-f, --filename <type>', 'Set filename to execute')

commander.parse();
const options = commander.opts();
//console.log(options.filename);

if (options.filename)
    filename = options.filename;
/**
 * 从文件中读取原始语料并通过回调函数开始处理
 * @param {type} filename 文件名
 * @param {type} callback 执行变量名回填的回调函数
 * @returns {undefined}
 */
var readFromFile = function (filename, callback) {
    var code = fs.readFile(filename, 'utf-8', function (err, data) {
        if (err){
            console.log('NISL ERROR OCCURED: ' + err);
            console.log("----------");
        }
        else {
            callback(data.toString());
        }
    });
};
console.log("------------------------------");
// // 规则1：随机代码块删除
var random_block_remove = function(source) {
    var ast = esprima.parse(source);
    let source_copy = escodegen.generate(ast);
    estraverse.traverse(ast, {
        enter: function (node, parent) {
            // 匹配函数体
            if(node.type == "VariableDeclarator" && node.id.name.includes("fuzzopt")){
                // 随机在函数体节点中选择一个不是变量声明的节点
                for(let i = 0; i < node.init.body.body.length; i++){
                    random_block_index = Math.floor(Math.random() * node.init.body.body.length);
                    if(node.init.body.body[random_block_index].type != "VariableDeclaration"){break;}
                }
                // 删除此节点
                node.init.body.body.splice(random_block_index, 1);
            }
        },
    });
    let codegen = escodegen.generate(ast);
    if(codegen != source_copy){
       console.log(codegen);
       console.log("random_block_remove");
       console.log("------------------------------");
   }
};

// // 规则2：While与If代码块互换
// var while_if_swap = function(source) {
//     var ast = esprima.parse(source);
//     let source_copy = escodegen.generate(ast);
//     let flag = 0;
//     estraverse.traverse(ast, {
//         enter: function (node){
//             // 匹配不包含else的if代码块
//             //if(node.type == "IfStatement" && node.alternate == undefined){
//             if(node.type == "IfStatement"){
//                 flag = 1;
//                 // 替换节点类型
//                 node.type = "WhileStatement";
//                 // 删除else节点
//                 delete node.alternate;
//                 //修改consequent属性为body
//                 node.body = node.consequent;
//                 delete node.consequent;
//             }
//             // 匹配while节点
//             if(node.type == "WhileStatement" && flag == 0){
//                 // 替换节点类型
//                 node.type = "IfStatement";
//                 //修改consequent属性为body
//                 node.consequent = node.body;
//                 delete node.body;
//                 // 增加else节点
//                 node.alternate = undefined;
//             }
//         },
//     });
//     let codegen = escodegen.generate(ast);
//     if(codegen != source_copy){
//        console.log(codegen);
//        console.log("while_if_swap");
//        console.log("------------------------------");
//    }
// };
//
//
// // 规则3：条件代码块包裹
// var condition_code_add = function(source) {
//     let while_code = "while(True){}";
//     let if_code = "if(True){}";
//     let while_ast = esprima.parse(while_code);
//     let if_ast = esprima.parse(if_code);
//     estraverse.traverse(while_ast, {
//         enter: function (node) {
//             if(node.type == "WhileStatement"){
//                     while_node = node;
//                 }
//         },
//     });
//     estraverse.traverse(if_ast, {
//         enter: function (node) {
//             if(node.type == "IfStatement"){
//                     if_node = node;
//                 }
//         },
//     });
//     var ast = esprima.parse(source);
//     let source_copy = escodegen.generate(ast);
//     estraverse.traverse(ast, {
//         enter: function (node) {
//             // 匹配函数体
//             if(node.type == "VariableDeclarator" && node.id.name.includes("NISLFuzzingFunc")){
//                 // 随机在函数体节点中选择一个不是变量声明的节点
//                 for(let i = 0; i < node.init.body.body.length; i++){
//                     random_block_index = Math.floor(Math.random() * node.init.body.body.length);
//                     if(node.init.body.body[random_block_index].type != "VariableDeclaration"){break;}
//                 }
//                 // 备份节点
//                 let node_copy = node.init.body.body[random_block_index];
//                 // 随机选择 if/while 包裹节点
//                 let node_arr = [while_node, if_node];
//                 node.init.body.body[random_block_index] = node_arr[Math.floor(Math.random() * node_arr.length)];
//                 // 随机生成条件值
//                 node.init.body.body[random_block_index].test.name = Boolean(Math.round(Math.random()));
//                 //原节点变为if/while代码体
//                 if(node.init.body.body[random_block_index].type == "WhileStatement"){
//                     node.init.body.body[random_block_index].body.body[0] = node_copy;
//                 }else{
//                     node.init.body.body[random_block_index].consequent.body[0] = node_copy;
//                 }
//                 // console.log(node);
//             }
//         },
//     });
//     let codegen = escodegen.generate(ast);
//     if(codegen != source_copy){
//        console.log(codegen);
//        console.log("condition_code_add");
//        console.log("------------------------------");
//    }
// };
//
// // 规则4：操作符替换
// var replaceOperator = function(source) {
//     var BinaryExpression = ["+", "-", "*", "/", "%", "==", "===", "!=", "!==", ">", "<", ">=", "<="];
//     var UpdateExpression = ["++", "--"];
//     var LogicalExpression = ["&&", "||"];
//     let flag = 0;
//     var ast = esprima.parse(source);
//     for(var i = 0; i<5 ; i++ ){
//         estraverse.traverse(ast, {
//             enter: function (node) {
//                 if(node.type == 'BinaryExpression'){
//                     flag = 1;
//                     node.operator = BinaryExpression[Math.floor(Math.random() * BinaryExpression.length)];
//                 }
//                 if(node.type == 'UpdateExpression'){
//                     flag = 1;
//                     node.operator = UpdateExpression[Math.floor(Math.random() * UpdateExpression.length)];
//                 }
//                 if(node.type == 'LogicalExpression'){
//                     flag = 1;
//                     node.operator = LogicalExpression[Math.floor(Math.random() * LogicalExpression.length)];
//                 }
//             },
//             leave: function (node, parent) {}
//         });
//         if(flag == 1) {
//             codegen = escodegen.generate(ast);
//             console.log(codegen);
//             console.log("replaceOperator");
//             console.log("------------------------------");
//         }
//     }
// };
//
// // TODO：代码增加规则（查看现有工具以及量子编译器代码增加方法）
//
readFromFile(filename, random_block_remove);
// readFromFile(filename, while_if_swap);
// readFromFile(filename, condition_code_add);
// readFromFile(filename, replaceOperator);