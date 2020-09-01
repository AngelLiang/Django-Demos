# 工作流程

## 工作流程创建步骤

进入【工作流程】创建页面，添加工作流程名称，选择工作流对象状态字段，给工作流程添加【流程状态】，比如可以添加如下状态：

- 草稿
- 打开
- 处理
- 完成
- 关闭

进入草稿状态的修改页面，选中【可编辑】，保存。

进入完成状态的修改页面，选中【可填写处理意见】，保存。

然后添加【流转元数据】：

- 草稿 -> 打开
- 打开 -> 处理
- 处理 -> 完成
- 完成 -> 关闭
- 完成 -> 打开

添加【批准元数据】：

- 名称打开，流转元数据为【草稿 -> 打开】
- 名称处理，流转元数据为【打开 -> 处理】
- 名称完成，流转元数据为【处理 -> 完成】
- 名称关闭，流转元数据为【完成 -> 关闭】
- 名称再关闭，流转元数据为【完成 -> 打开】

添加完【批准元数据】后，检查状态的起始状态和结束状态是否正确。

## 备份配置和必要的数据

    $ python manage.py dumpdata rworkflow.workflow rworkflow.workflowcategory rworkflow.transitionapprovalmeta rworkflow.transitionmeta rworkflow.state organization hr auth.user -o fixtures\initdata.json

## 恢复配置和必要的数据

    $ python manage.py loaddata fixtures\initdata.json

