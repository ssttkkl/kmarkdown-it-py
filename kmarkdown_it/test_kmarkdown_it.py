def test_extract_plain_text():
    from kmarkdown_it import KMarkdownIt

    doc = """**KOOK**
专属游戏玩家的*文字、语音和组队工具*

(ins)安全免费(ins)，(ins)没有广告(ins)，(ins)低资源占用(ins)，(ins)高通话质量(ins)(emj)haha(emj)[233]
KOOK是最好的~~语音~~软件
(chn)114514(chn): (met)1919810(met)

~~(rol)狗管理(rol)~~

[KOOK](https://kookapp.cn)
`/help`
(spl)Talk is cheap.Make it happen.(spl)

```js
function factorial(n, total) {
    if (n === 1) return total;
    return factorial(n - 1, n * total);
}

factorial(5)
```

> Talk is cheap.
Make it Happen.

---
"""

    exc = """KOOK
专属游戏玩家的文字、语音和组队工具

安全免费，没有广告，低资源占用，高通话质量
KOOK是最好的语音软件
: 



KOOK
/help
Talk is cheap.Make it happen.

function factorial(n, total) {
    if (n === 1) return total;
    return factorial(n - 1, n * total);
}

factorial(5)

Talk is cheap.
Make it Happen.
"""

    kmd_it = KMarkdownIt()
    act = kmd_it.extract_plain_text(doc)
    assert act == exc



