遗传算法 GA Edition：2  
GAmain：主函数  
Cross:遗传算子交叉函数  
Decode：遗传算子解码函数（二进制变成十进制）  
Encode：遗传算子编码函数（十进制变成二进制）  
InitPopulation:初始化种群函数  
Select：选择遗传算子进入交配池的函数  
Variate:遗传算子变异函数  
f:优化目标函数  
  
思路：  
初始化种群  
评分  
轮盘赌选交配池  
交叉  
变异  
不断迭代直到特定代数  
