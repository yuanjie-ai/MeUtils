#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : chatgpt
# @Time         : 2023/3/2 下午5:12
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import requests

prompt = "周杰伦"
json = {
    "prompt": prompt,
    "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2NDAwNjVjZWVmZmM2ZWQwNjNkMTA3NmMiLCJhdWQiOiI2M2VkNzg1YmQ0YzVlMWFhMGU5NDkzYmMiLCJpYXQiOjE2Nzc3NDc2NjQsImV4cCI6MTY3ODk1NzI2NCwiaXNzIjoiaHR0cHM6Ly9jaGF0LWdwdC5hdXRoaW5nLmNuL29pZGMiLCJub25jZSI6IjI3NzA1MTE4MjI1MjYwMTQiLCJuYW1lIjpudWxsLCJnaXZlbl9uYW1lIjpudWxsLCJtaWRkbGVfbmFtZSI6bnVsbCwiZmFtaWx5X25hbWUiOm51bGwsIm5pY2tuYW1lIjpudWxsLCJwcmVmZXJyZWRfdXNlcm5hbWUiOm51bGwsInByb2ZpbGUiOm51bGwsInBpY3R1cmUiOiJodHRwczovL2ZpbGVzLmF1dGhpbmcuY28vYXV0aGluZy1jb25zb2xlL2RlZmF1bHQtdXNlci1hdmF0YXIucG5nIiwid2Vic2l0ZSI6bnVsbCwiYmlydGhkYXRlIjpudWxsLCJnZW5kZXIiOiJVIiwiem9uZWluZm8iOm51bGwsImxvY2FsZSI6bnVsbCwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMDJUMDk6MDE6MDIuNjYzWiIsImVtYWlsIjpudWxsLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInBob25lX251bWJlciI6IjE4NTUwMjg4MjMzIiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjp0cnVlLCJhZGRyZXNzIjp7ImNvdW50cnkiOm51bGwsInBvc3RhbF9jb2RlIjpudWxsLCJyZWdpb24iOm51bGwsImZvcm1hdHRlZCI6bnVsbH19.pELqWd6EBcqhC5bkxLiWZzoj9eS0KHHbiCTA9I-ep8E"
}
r = requests.post("https://youqianmeidifanghua.online/chat", json=json)

# print(r.json())

for c in r.json()['choices']:
    print(c['message']['content'])
