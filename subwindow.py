from time import sleep
from threading import Timer

import flet
from flet import ListView, Page, Text
from screeninfo import get_monitors
DisplayMargin = 60
Width_SubWindow = 400
TitleBar_Height = 26


class SubWindow():
    def __init__(self, title):
        self.title = title
    page = None

    def destroy(self):
        if not (self.page == None):
            self.page.window_destroy()

    def main(self, page: Page):
        page.title = self.title
        page.window_always_on_top = True
        page.theme_mode = "dark"
        dispHeight = 0
        dispWidth = 0
        for m in get_monitors():
            if m.is_primary:
                # screenName = m.name
                dispWidth = m.width
                dispHeight = m.height

        page.window_left = dispWidth-Width_SubWindow-DisplayMargin
        page.window_top = DisplayMargin
        page.window_width = Width_SubWindow
        page.window_height = dispHeight-DisplayMargin*2-TitleBar_Height

        # page.window_prevent_close = True
        self.page = page

        # page.window_minimized = True

        def window_event_handler(e):
            print("dd")
            # if e.data == 'close':
            #    self.page.window_destroy()
            # el
            if e.data == 'minimize':
                # page.window_minimized = True
                self.page.window_destroy()
                self.page.window_close()

            # app_close(e.page)
                page.update()
        page.on_window_event = window_event_handler

        def createListTile(str, myself):
            if myself:
                return flet.Card(
                    content=flet.ListTile(
                        opacity=1.0,
                        leading=flet.Image(
                            src="./default.png", fit="contain"),
                        title=flet.Text(
                            str,
                            selectable=True,

                            text_align=flet.TextAlign.LEFT,
                        ),
                    )
                )
            else:
                return flet.Card(
                    margin=flet.Margin(left=100, top=1, right=0, bottom=0),
                    content=flet.ListTile(
                        opacity=1.0,
                        trailing=flet.Image(
                            src="./default.png", fit="contain"),
                        title=flet.Text(
                            str,
                            selectable=True, text_align=flet.TextAlign.LEFT, ),
                    ),
                )

        def createTab():
            eachChatList = flet.Column(
                spacing=10,
                # padding=20,
                expand=1,
                auto_scroll=True,
                scroll=flet.ScrollMode.ADAPTIVE,

                controls=[]
            )
            roleTextField = flet.TextField(
                visible=False,
                expand=False,
                label="ロール:",
                multiline=True,
                disabled=False,
                value="line1",
                border_color="white",

                # on_submit=button_clickedd
                # on_change=button_clickedd,
            )

            def roleExpandCtl(e):
                roleExpandCtlEx(e)
            roleIcon = flet.IconButton(
                icon=flet.icons.EXPAND_LESS,
                on_click=roleExpandCtl
            )

            def close_dlg(e):
                dlg_modal.open = False
                page.update()
            dlg_modal = flet.AlertDialog(
                modal=True,
                # title=flet.Text("Please confirm"),
                content=flet.DataTable(
                    columns=[
                        flet.DataColumn(flet.Text("First name")),
                        flet.DataColumn(flet.Text("Last name")),
                        flet.DataColumn(flet.Text("Age"), numeric=True),
                    ],
                    rows=[
                        flet.DataRow(
                            cells=[
                                flet.DataCell(flet.Text("John")),
                                flet.DataCell(flet.Text("Smith")),
                                flet.DataCell(flet.Text("43")),
                            ],
                        ),
                        flet.DataRow(
                            cells=[
                                flet.DataCell(flet.Text("Jack")),
                                flet.DataCell(flet.Text("Brown")),
                                flet.DataCell(flet.Text("19")),
                            ],
                        ),
                        flet.DataRow(
                            cells=[
                                flet.DataCell(flet.Text("Alice")),
                                flet.DataCell(flet.Text("Wong")),
                                flet.DataCell(flet.Text("25")),
                            ],
                        ),
                    ],
                ),
                actions=[
                    flet.TextButton("Yes", on_click=close_dlg),
                    flet.TextButton("No", on_click=close_dlg),
                ],
                actions_alignment=flet.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )

            def open_dlg_modal(e):
                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()
            roleSelectBtn = flet.FilledButton(on_click=open_dlg_modal,
                                              text="ロール選択")

            def roleExpandCtlEx(e):
                visiblew = not roleTextField.visible
                chgroleExpand(visiblew)

            def chgroleExpand(visiblew):
                if visiblew:
                    roleTextField.visible = visiblew
                    roleSelectBtn.visible = visiblew
                    roleIcon.icon = flet.icons.EXPAND_MORE
                else:
                    roleTextField.visible = visiblew
                    roleSelectBtn.visible = visiblew
                    roleIcon.icon = flet.icons.EXPAND_LESS
                page.update()

            def deleteTab(e):
                deleteTabEx()

            promptField = flet.TextField(
                expand=1,
                label="プロンプト:",
                multiline=True,
                disabled=False,
                value="line1",
                border_color="white",

                # on_submit=button_clickedd
                # on_change=button_clickedd,
            )
            temporaryChat = createListTile("会話を始めましょう。↑でロールを設定できますよ！", True)
            eachChatList.controls.append(
                temporaryChat
            ),

            def apply(e):
                txt = promptField.value

                if len(txt) > 0:
                    if len(roleTextField.value) == 0:
                        page.snack_bar = flet.SnackBar(
                            content=flet.Text("ロールを設定してください。"),
                            # action="Alright!",
                        )
                        page.snack_bar.open = True
                        page.update()
                        return
                    if (len(eachChatList.controls) == 1) and (eachChatList.controls[0] == temporaryChat):
                        eachChatList.controls.clear()
                        chgroleExpand(False)

                    eachChatList.controls.append(
                        createListTile(txt, False)
                    ),

                    promptField.value = ""
                    promptField.focus()
                    self.page.update()
                else:
                    promptField.focus()
                # time = Timer(5, xx)
                # time.start()
            chgroleExpand(True)
            tab = flet.Tab(
                tab_content=flet.Icon(flet.icons.SUPPORT_AGENT,),
                content=flet.Column(expand=True,
                                    controls=[
                                        flet.Card(content=flet.Column(horizontal_alignment=flet.CrossAxisAlignment.START, expand=False, controls=[
                                            flet.Row(controls=[roleIcon,
                                                               roleSelectBtn,

                                                               flet.Container(
                                                                   expand=True),
                                                               flet.FilledButton(on_click=deleteTab,
                                                                                 text="削除"),]),
                                            roleTextField
                                        ]

                                        )),
                                        flet.Container(expand=True, border=flet.Border(
                                            top=flet.BorderSide(
                                                width=1, color="white"),
                                            bottom=flet.BorderSide(
                                                width=1, color="white"),
                                            right=flet.BorderSide(
                                                width=1, color="white"),
                                            left=flet.BorderSide(width=1, color="white")),
                                            content=eachChatList),
                                        flet.Row(controls=[
                                            promptField,
                                            flet.IconButton(icon=flet.icons.SEND,
                                                            on_click=apply,
                                                            expand=0,),
                                        ]),

                                    ])


            )

            def deleteTabEx():
                self.tabs.tabs.remove(tab)
                print("hoge")
                if len(self.tabs.tabs) == 1:
                    self.tabs.tabs.insert(0, createTab())
                page.update()
            return tab

        def tabchange(e: flet.ControlEvent):

            # print(e)
            # print(e.page)
            # print(e.target)
            # print(e.data)
            # print(e.control)
            # print(e.name)
            # print(len(self.tabs.tabs)-1)

            if int(e.data) == len(self.tabs.tabs)-1:
                self.tabs.tabs.insert(0, createTab())

                # def selectTab():
                #    print("tab")
                #    self.tabs.selected_indexs = len(self.tabs.tabs)-2
                #    page.update()

                # time = Timer(2, selectTab)
                # time.start()
                page.update()

        self.tabs = flet.Tabs(selected_index=0,
                              animation_duration=300, tabs=[
                                  createTab(),
                                  flet.Tab(tab_content=flet.Icon(
                                      flet.icons.ADD), )
                              ],
                              expand=1, on_change=tabchange)

        page.add(
            # flet.Column(spacing=0, scroll=flet.ScrollMode.HIDDEN, controls=[

            self.tabs,

            #    ]
        )
