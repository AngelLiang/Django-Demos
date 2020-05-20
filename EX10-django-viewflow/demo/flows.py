from viewflow import flow
from viewflow import frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from .models import HelloWorldProcess


@frontend.register
class HelloWorldFlow(Flow):
    process_class = HelloWorldProcess

    # 开始
    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    # 分配
    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    # 检查分配
    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    # 发送
    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    # 结束
    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)
