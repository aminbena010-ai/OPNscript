grammar OPN;

program: (functionDecl | mainBlock)+ EOF;

functionDecl: FUNC IDENT LPAREN paramList? RPAREN block;
mainBlock: MAIN block;

paramList: IDENT (COMMA IDENT)*;

block: LBRACE statement* RBRACE;

statement
    : letStatement
    | setStatement
    | returnStatement
    | ifStatement
    | forStatement
    | expressionStatement
    ;

letStatement: LET IDENT EQUAL expression SEMICOLON;
setStatement: SET IDENT EQUAL expression SEMICOLON;
returnStatement: RETURN expression? SEMICOLON;
ifStatement: IF expression block (ELSE block)?;
forStatement: FOR IDENT IN expression (RANGE expression)? block;
expressionStatement: expression SEMICOLON;

expression: logicalOr;
logicalOr: logicalAnd (OR logicalAnd)*;
logicalAnd: equality (AND equality)*;
equality: comparison ((EQ | NEQ) comparison)*;
comparison: addition ((LT | LTE | GT | GTE) addition)*;
addition: multiplication ((PLUS | MINUS) multiplication)*;
multiplication: unary ((STAR | SLASH) unary)*;
unary: (NOT | MINUS) unary | call;
call: primary (LPAREN argumentList? RPAREN | DOT IDENT)*;
argumentList: expression (COMMA expression)*;
primary: NUMBER | STRING | TRUE | FALSE | IDENT | LPAREN expression RPAREN;

LET: 'let';
SET: 'set';
RETURN: 'return';
FUNC: 'func';
MAIN: 'main';
IF: 'if';
ELSE: 'else';
FOR: 'for';
IN: 'in';
TRUE: 'true';
FALSE: 'false';
AND: 'and';
OR: 'or';
NOT: 'not';
EQ: '==';
NEQ: '!=';
LTE: '<=';
GTE: '>=';
LT: '<';
GT: '>';
RANGE: '..';
PLUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';
EQUAL: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
SEMICOLON: ';';
COMMA: ',';
DOT: '.';
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' (~["\\] | '\\' .)* '"';
IDENT: [a-zA-Z_] [a-zA-Z0-9_]*;
COMMENT: '#' ~[\r\n]* -> skip;
WS: [ \t\r\n]+ -> skip;
