
//判断对象,数组,字符串等是否为空
function isNull(obj) {
    let str = String(obj)
    if (str === 'undefined' || str === 'null' || str === '' || !str || !/[^\s]/.test(str)) {
        return true
    }
    console.log(typeof obj)
    if (typeof obj === 'object') {
        let json = JSON.stringify(obj)
        if (json === '{}') {
            return true
        }
        if (json === '[]') {
            return true
        }
        return false
    } else {
        return false
    }
}

// 控制台日志,支持传一个参数(对象/字符串), 也支持传两个参数(标志,日志消息<可以是对象,可以是字符串>)
function clog(flag, value = 'xxxxxxxxxxxxxxxxxxx=Default-value_override+xxxxxxxxxxxxxxxxx') {
    try {
        // 如果value为默认值,则没有传递第二个参数,只处理第一个参数
        if (value === `xxxxxxxxxxxxxxxxxxx=Default-value_override+xxxxxxxxxxxxxxxxx`) {
            let tmp = JSON.stringify(flag);
            console.log(tmp)
        } else if (isNull(value)) {
            let tmp = JSON.stringify(flag);
            console.log(tmp + ":")
        } else if (isNull(flag)) {
            let tmp = JSON.stringify(value);
            console.log(":" + tmp)
        } else {
            let tmp = JSON.stringify(value);
            console.log(flag + ":" + tmp)
        }
    } catch (err) {
        console.log("log", err)
    }
}

//批量导入局部组件 (批量导入全局组件参见vue官网)
//使用方法 components: importComponents(require.context('./', false, /Yi.*\.vue$/)),  // 导入当前目录以"Yi" 开头,以".vue"结尾的全部组件
//require.context('./components', false, /Yi.*\.vue$/) : webpack的方法, 第一个参数为文件路径, 第二个参数为是否包含子文件夹, 第三个参数为正则
function importComponents(comps) {
    let res_components = {}
    comps.keys().forEach((fileName) => {
        let comp = comps(fileName)
        res_components[fileName.replace(/^\.\/(.*)\.\w+$/, '$1')] = comp.default
    })
    return res_components
}

//获取当前时间, 出参为格式化后的日期字符串
function timeNow() {
    let time = new Date();  // 程序计时的月从0开始取值后+1  
    let m = time.getMonth() + 1;
    let t = time.getFullYear() + "-" + m + "-" + time.getDate() + " " + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds();
    return t;
}

//一天的开始, 入参为Date类型, 出参为格式化后的日期字符串
function timeDayBegin(time) {
    let m = time.getMonth() + 1;
    let t = time.getFullYear() + "-" + m + "-" + time.getDate() + " 00:00:00";
    return t;
}

//一天的结束, 入参为Date类型, 出参为格式化后的日期字符串
function timeDayEnd(time) {
    let m = time.getMonth() + 1;
    let t = time.getFullYear() + "-" + m + "-" + time.getDate() + " 23:59:59";
    return t;
}


//字符串数组转整型数字键
function strArr2IntArr(arrStr) {
    for (let i = 0; i < arrStr.length; i++) {
        arrStr[i] = parseFloat(arrStr[i])
    }
    return arrStr;
}

