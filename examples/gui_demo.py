#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : gui_demo
# @Time         : 2021/3/3 2:45 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


# import PySimpleGUI as sg
#
# sg.theme('DarkAmber')   # Add a touch of color
# # All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]
#
# # Create the Window
# window = sg.Window('Window Title', layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])
#
# window.close()
#
# import PySimpleGUI as sg
#
# # Create some widgets
# ok_btn = sg.Button('Open Second Window')
# cancel_btn = sg.Button('Cancel')
# layout = [[ok_btn, cancel_btn]]
#
# # Create the first Window
# window = sg.Window('Window 1', layout)
#
# win2_active = False
#
# # Create the event loop
# while True:
#     event1, values1 = window.read(timeout=100)
#
#     if event1 in (None, 'Cancel'):
#         # User closed the Window or hit the Cancel button
#         break
#
#     if not win2_active and event1 == 'Open Second Window':
#         win2_active = True
#         layout2 = [[sg.Text('Window 2')],
#                    [sg.Button('Exit')]]
#
#         window2 = sg.Window('Window 2', layout2)
#
#     if win2_active:
#         events2, values2 = window2.Read(timeout=100)
#         if events2 is None or events2 == 'Exit':
#             win2_active = False
#             window2.close()
#
# window.close()


import PySimpleGUI as sg

sg.theme('Dark Blue 3')  # please make your creations colorful

layout = [[sg.Text('Filename')],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK(), sg.Cancel()]]

window = sg.Window('Get filename example', layout)

event, values = window.read()
print(event, values)
window.close()
