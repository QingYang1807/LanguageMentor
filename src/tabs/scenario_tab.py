# tabs/scenario_tab.py

import gradio as gr
from agents.scenario_agent import ScenarioAgent
from utils.logger import LOG

# 初始化场景代理
agents = {
    "job_interview": ScenarioAgent("job_interview"),
    "hotel_checkin": ScenarioAgent("hotel_checkin"),
    "salary_negotiation": ScenarioAgent("salary_negotiation"),
    "renting": ScenarioAgent("renting"),
    "leave_request": ScenarioAgent("leave_request"),
    "baggage_checkin": ScenarioAgent("baggage_checkin"),
    "car_rental": ScenarioAgent("car_rental"),
    "dining_out": ScenarioAgent("dining_out"),
    "travel_planning": ScenarioAgent("travel_planning"),
    "rideshare": ScenarioAgent("rideshare"),
    "resume_preparation": ScenarioAgent("resume_preparation"),
    "dating": ScenarioAgent("dating"),
    # 可以根据需要添加更多场景代理
}

def get_page_desc(scenario):
    try:
        with open(f"content/page/{scenario}.md", "r", encoding="utf-8") as file:
            scenario_intro = file.read().strip()
        return scenario_intro
    except FileNotFoundError:
        LOG.error(f"场景介绍文件 content/page/{scenario}.md 未找到！")
        return "场景介绍文件未找到。"
    
# 获取场景介绍并启动新会话的函数
def start_new_scenario_chatbot(scenario):
    initial_ai_message = agents[scenario].start_new_session()  # 启动新会话并获取初始AI消息

    return gr.Chatbot(
        value=[(None, initial_ai_message)],  # 设置聊天机器人的初始消息
        height=600,  # 聊天窗口高度
    )

# 场景代理处理函数，根据选择的场景调用相应的代理
def handle_scenario(user_input, chat_history, scenario):
    bot_message = agents[scenario].chat_with_history(user_input)  # 获取场景代理的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录场景代理的回复
    return bot_message  # 返回场景代理的回复

def create_scenario_tab():
    with gr.Tab("场景"):  # 场景标签
        gr.Markdown("## 选择一个场景完成目标和挑战")  # 场景选择说明

        # 创建单选框组件
        scenario_radio = gr.Radio(
            choices=[
                ("求职面试", "job_interview"),  # 求职面试选项
                ("酒店入住", "hotel_checkin"),  # 酒店入住选项
                ("薪资谈判", "salary_negotiation"),  # 薪资谈判选项
                ("租房", "renting"),  # 租房选项
                ("单位请假", "leave_request"),  # 单位请假选项
                ("机场托运", "baggage_checkin"),  # 机场托运选项
                ("自驾租车", "car_rental"),  # 自驾租车选项
                ("聚餐吃饭", "dining_out"),  # 聚餐吃饭选项
                ("出行旅游", "travel_planning"),  # 出行旅游选项
                ("滴滴打车", "rideshare"),  # 滴滴打车选项
                ("准备简历", "resume_preparation"),  # 准备简历选项
                ("恋爱约会", "dating")  # 恋爱约会选项
            ],
            label="场景"  # 单选框标签
        )

        scenario_intro = gr.Markdown()  # 场景介绍文本组件
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",  # 聊天机器人的占位符
            height=600,  # 聊天窗口高度
        )

        # 更新场景介绍并在场景变化时启动新会话
        scenario_radio.change(
            fn=lambda s: (get_page_desc(s), start_new_scenario_chatbot(s)),  # 更新场景介绍和聊天机器人
            inputs=scenario_radio,  # 输入为选择的场景
            outputs=[scenario_intro, scenario_chatbot],  # 输出为场景介绍和聊天机器人组件
        )

        # 场景聊天界面
        gr.ChatInterface(
            fn=handle_scenario,  # 处理场景聊天的函数
            chatbot=scenario_chatbot,  # 聊天机器人组件
            additional_inputs=scenario_radio,  # 额外输入为场景选择
            retry_btn=None,  # 不显示重试按钮
            undo_btn=None,  # 不显示撤销按钮
            clear_btn="清除历史记录",  # 清除历史记录按钮文本
            submit_btn="发送",  # 发送按钮文本
        )
