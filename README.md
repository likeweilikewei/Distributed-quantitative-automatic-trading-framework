# Distributed-quantitative-automatic-trading-framework
Ensure high concurrency, accuracy, and reliability of automated trading of stock strategies
相对于普通的量化框架，本架构有如下特点：
1. 应用观察者模式保证运行时数据一致性，利用执行日志实现异常数据一致性；
2.通过区分交易流程、指标判断，实现 1000+前端选项指标的极其复杂交易逻辑；
3.构建分布式任务队列，实现高并发，保证 1W+策略 2h 内交易完毕；
4.充分利用缓存、显著提升查询速度，提高程序鲁棒性；
5.应用单例模式实现 Redis 连接，利用事件驱动实现异步 IO，利用管道优化通信时间；
6.防御式编程，提高接口鲁棒性；
