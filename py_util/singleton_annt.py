#!/usr/bin/env python
# -*- coding: utf8 -*-



# 【术语】 SngltAnnt == SingletonAnnotation == 单例注解

#参考: https://blog.csdn.net/chenyongfa188/article/details/105612341

#Python 装饰器线程安全单例的实现(使用函数装饰器)
import threading
import time
def funcSngltAnnt(cls):
    instance = {}
    lock = threading.Lock()

    def __single_with_thread_lock(*args,**kwargs): # args、kwargs 中放的是 __BuszClz000__.__init__的参数们
        # print("lock" + str(lock)) #全都是同一个lock
        if cls not in instance:
            with lock:
                if cls not in instance:
                    instance[cls] = cls(*args,**kwargs)
        return instance[cls]
    return __single_with_thread_lock

@funcSngltAnnt
class __BuszClz000__:
#以上两行 等价于 funcSngltAnnt(class __BuszClz000__)
#意思是说 'class __BuszClz000__'的任何访问 都被 funcSngltAnnt 多包裹了一层
    def __init__(self,age:int):
        #此__init__方法只会进入一次
        self.m_age:int=age
        time.sleep(2)
        print(f"self.m_age={self.m_age}")
    
    @staticmethod
    def static_method():
        pass

def printNewInstance():
    import random
    inst=__BuszClz000__(random.randint(4,10))
    # print(inst) #都是类__C000__的同一个实例
    print(f"inst.m_age={inst.m_age}") #这里打印的都是99



#以下是测试单例模式
if __name__=="__main__":
    __BuszClz000__(99)#此行为第一次调用  方法__C000__.__init__ , 会实际进入到 方法__C000__.__init__
    for i in range(20):
        threading.Thread(target=printNewInstance).start()
    
    __BuszClz000__.static_method() #此行报错 AttributeError: 'function' object has no attribute 'static_method'
    #  由于 '@funcSngltAnnt  class __BuszClz000__' == funcSngltAnnt(class __BuszClz000__)
    # 因此 这种模式之下 实际上已经无法拿到 真实类对象__BuszClz000__了 
    
