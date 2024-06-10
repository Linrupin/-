var _ = "web";
var w = "Mk6hqtUp33DGGtoS63tTJbMUYjRrG1Lu";
var v = "webdict";
const Crypto = require("crypto-js");
function h(r){
    return  Crypto.MD5(r).toString();
}
function jiemi(text){
    r = "".concat(text).concat(v);
    o = h(r);
    time = "".concat(text).concat(v).length % 10;
    n = "".concat(_).concat(text).concat(time).concat(w).concat(o);
    console.log(n)
    return Crypto.MD5(n).toString();
}
a = jiemi("牛马");
console.log(a)
