// npm install --save-dev @babel/core commander --registry=http://registry.npmmirror.com


const babel = require("@babel/core");

function fixReturn(source_code) {

    const babel = require('@babel/core');
    const ast = babel.parse(source_code, {
        sourceType: 'module'
    });


    let returnState = ''


//输出所有定义的变量和对应的类型
    babel.traverse(ast, {
        enter(path) {
            if (path.node.type === "FunctionDeclaration" && path.node.id.name === "fuzzopt") {
                //方法内部
                let funcbody = path.node.body.body

                for (let i = 0; i < funcbody.length; i++) {
                    if (funcbody[i].type === "VariableDeclaration") {
                        let varValue = funcbody[i].declarations[0]
                        if (varValue.init.type === "NewExpression") {
                            if (varValue.init.callee.name == "Map" || varValue.init.callee.name == "Set") {
                                returnState += "..." + varValue.id.name + ","
                            }
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',callee is ' + varValue.init.callee.name)
                        } else if (varValue.init.type === "ObjectExpression") {
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, '属性使用动态解析')
                            // returnState += 'Object.entries('+varValue.id.name+'),'
                            returnState += 'JSON.stringify(' + varValue.id.name + '),'
                        }
                        //布尔，undefined
                        else if (varValue.init.type === "Identifier") {
                            returnState += varValue.id.name + ','
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',value is ' + varValue.init.name)
                        } else if (varValue.init.type === "BooleanLiteral") {
                            // console.log(varValue)
                            returnState += varValue.id.name + ','
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',value is ' + varValue.init.value)
                        } else if (varValue.init.type === "NullLiteral") {
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',value is null')
                            returnState += varValue.id.name + ','
                        } else if (varValue.init.type === "RegExpLiteral") {
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',value is ' + varValue.init.pattern)
                            returnState += varValue.id.name + ','
                        } else if (varValue.init.type === "ArrayExpression") {
                            // console.log(varValue)
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',length is ' + varValue.init.elements.length)
                            returnState += varValue.id.name + ','
                        } else if (varValue.init.type === "BinaryExpression") {
                            // console.log(varValue)
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',value is ' + varValue.init.value)
                            returnState += varValue.id.name + ','

                        } else {
                            console.log('name is ' + varValue.id.name, ',type is ' + varValue.init.type, ',value is ' + varValue.init.value)
                            returnState += varValue.id.name + ','
                        }
                    }
                }
            }
            if (path.node.type === "ReturnStatement" && returnState.length != 0) {
                path.remove()
            }
        }
    });

    console.log(returnState)
    if (returnState.length != 0) {
        returnState = 'return [' + returnState + ']'
        const CONSOLE_AST = babel.template.ast(returnState);
        babel.traverse(ast, {
            enter(path) {
                if (path.node.type === "FunctionDeclaration" && path.node.id.name === "fuzzopt") {
                    const blockStatementBody = path.node.body.body;
                    if (blockStatementBody && blockStatementBody.length) {
                        const index = blockStatementBody.length;
                        if (~index) {
                            blockStatementBody.splice(index, 0, CONSOLE_AST); // 直接修改 ast, 前插⼀个节 点
                        }
                    }
                }
            }
        });
    }


    // console.log(babel.transformFromAstSync(ast).code);

    return babel.transformFromAstSync(ast).code
}

// readFromFile(filename, fixReturn);