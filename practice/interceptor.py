import json
from functools import cache

from mitmproxy import http


@cache
def load_js(filename):
	with open(filename, "r") as f:
		return f.read()


def response(flow: http.HTTPFlow) -> None:
	# 如果是练习场模式则替换答案全部为 1
	pattern = "https://xyks.yuanfudao.com/leo-math/android/exams?"
	if pattern in flow.request.url:
		data = flow.response.json()
		questions = data["questions"]
		replaced_questions = []
		for q in questions:
			q['answer'] = '1'
			q['answers'] = ['1']
			replaced_questions.append(q)
		data["questions"] = replaced_questions
		print(data)
		flow.response.text = json.dumps(data)

	# pk 场则劫持判题 js 文件，让所有的题目都判断为正确
	if "leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_" in flow.request.url and ".js" in flow.request.url:
		flow.response.text = load_js("exercise.js")
		print("intercept js")
