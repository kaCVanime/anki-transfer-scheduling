from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *


class TransferConfigWindow(QWidget):
    selected_src_deck = ""
    selected_target_deck = ""
    selected_src_field = ""
    selected_target_field = ""
    deck_list = []
    model_list = []
    src_field_list = []
    target_field_list = []
    rows = []
    transfer_rows = []

    def __init__(self, deck_name_list, model_list):
        super(TransferConfigWindow, self).__init__()
        self.deck_list = deck_name_list
        self.model_list = model_list

        self.v_layout = QVBoxLayout(self)

        self.groupbox_deck = QGroupBox('1. Choose Deck')
        self.form_layout_deck = QFormLayout(self)
        self.combobox_src_deck = QComboBox(self)
        self.combobox_target_deck = QComboBox(self)

        self.scroll_area_rows = QScrollArea(self)
        self.groupbox_rows = QGroupBox('2. Add group')
        self.v_layout_rows = QVBoxLayout(self)

        self.h_layout_row_btn = QHBoxLayout()
        self.add_row_btn = QPushButton(self)
        self.add_row_btn.setText("Add")
        self.remove_row_btn = QPushButton(self)
        self.remove_row_btn.setText("Remove")

        self.start_btn = QPushButton(self)
        self.start_btn.setText("Start")
        self.console = QTextEdit(self)
        # self.v_layout = QFormLayout(self)
        self.layout_init()
        self.combobox_init()
        self.add_row()

        if not len(deck_name_list):
            showInfo("there is no deck in your collection")

    def layout_init(self):
        self.v_layout.addWidget(self.groupbox_deck)
        self.v_layout.addWidget(self.scroll_area_rows)
        self.v_layout.addLayout(self.h_layout_row_btn)
        self.v_layout.addWidget(self.start_btn)
        self.v_layout.addWidget(self.console)

        self.groupbox_deck.setLayout(self.form_layout_deck)
        self.form_layout_deck.addRow("Source deck", self.combobox_src_deck)
        self.form_layout_deck.addRow("Target deck", self.combobox_target_deck)

        self.scroll_area_rows.setWidget(self.groupbox_rows)
        self.groupbox_rows.setLayout(self.v_layout_rows)
        self.scroll_area_rows.setWidgetResizable(True)
        self.scroll_area_rows.setFixedHeight(300)
        self.scroll_area_rows.setMinimumWidth(700)

        self.h_layout_row_btn.addWidget(self.remove_row_btn)
        self.h_layout_row_btn.addWidget(self.add_row_btn)

        self.setLayout(self.v_layout)

        self.start_btn.clicked.connect(lambda: self.start())
        self.add_row_btn.clicked.connect(lambda: self.add_row())
        self.remove_row_btn.clicked.connect(lambda: self.remove_row())

    def combobox_init(self):
        self.combobox_src_deck.addItems(self.deck_list)
        self.combobox_src_deck.currentIndexChanged.connect(
            lambda: self.on_deck_selected(self.combobox_src_deck, 'src'))
        self.on_deck_selected(self.combobox_src_deck, 'src')
        self.combobox_target_deck.addItems(self.deck_list)
        self.combobox_target_deck.currentIndexChanged.connect(
            lambda: self.on_deck_selected(self.combobox_target_deck, 'target'))
        self.on_deck_selected(self.combobox_target_deck, 'target')

    def remove_row(self):
        if len(self.rows) > 1:
            row = self.rows.pop()
            self.transfer_rows.pop()
            self.v_layout_rows.removeWidget(row)

    def add_row(self):
        groupbox_row = QGroupBox('transfer group')
        h_layout_row = QHBoxLayout()

        groupbox_row_model = QGroupBox('Choose note type')
        form_layout_row_model = QFormLayout(self)
        combobox_src_model = QComboBox(self)
        combobox_target_model = QComboBox(self)

        groupbox_row_compare = QGroupBox('Choose comparing field')
        form_layout_row_compare = QFormLayout(self)
        combobox_src_compare_field = QComboBox(self)
        combobox_target_compare_field = QComboBox(self)

        groupbox_row_card = QGroupBox('Choose card template')
        form_layout_row_card = QFormLayout(self)
        combobox_src_card = QComboBox(self)
        combobox_target_card = QComboBox(self)

        groupbox_row.setLayout(h_layout_row)
        h_layout_row.addWidget(groupbox_row_model)
        h_layout_row.addWidget(groupbox_row_compare)
        h_layout_row.addWidget(groupbox_row_card)

        groupbox_row_model.setLayout(form_layout_row_model)
        form_layout_row_model.addRow("src", combobox_src_model)
        form_layout_row_model.addRow("target", combobox_target_model)

        groupbox_row_compare.setLayout(form_layout_row_compare)
        form_layout_row_compare.addRow("src", combobox_src_compare_field)
        form_layout_row_compare.addRow("target", combobox_target_compare_field)

        groupbox_row_card.setLayout(form_layout_row_card)
        form_layout_row_card.addRow("src", combobox_src_card)
        form_layout_row_card.addRow("target", combobox_target_card)

        combobox_src_model.addItems(self.model_list)
        combobox_src_model.currentIndexChanged.connect(
            lambda: self.on_model_selected(combobox_src_model, combobox_src_compare_field, combobox_src_card))
        combobox_target_model.addItems(self.model_list)
        combobox_target_model.currentIndexChanged.connect(
            lambda: self.on_model_selected(combobox_target_model, combobox_target_compare_field, combobox_target_card))

        combobox_src_compare_field.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(groupbox_row, combobox_src_compare_field, "src_compare_field"))
        combobox_target_compare_field.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(groupbox_row, combobox_target_compare_field,
                                                    "target_compare_field"))

        combobox_src_card.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(groupbox_row, combobox_src_card, "src_card"))
        combobox_target_card.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(groupbox_row, combobox_target_card, "target_card"))

        self.v_layout_rows.addWidget(groupbox_row)
        self.rows.append(groupbox_row)
        self.transfer_rows.append(
            {"src_compare_field": "", "target_compare_field": "", "src_card": "", "target_card": ""})
        self.on_model_selected(combobox_src_model, combobox_src_compare_field, combobox_src_card)
        self.on_model_selected(combobox_target_model, combobox_target_compare_field, combobox_target_card)

    def on_deck_selected(self, combobox, type):
        label = combobox.currentText()
        if type == 'src':
            self.selected_src_deck = label
        else:
            self.selected_target_deck = label

    def on_model_selected(self, model_box, compare_box, card_box):
        model_name = model_box.currentText()
        if model_name:
            model = mw.col.models.by_name(model_name)
            fields = mw.col.models.field_names(model)
            templates = [m["name"] for m in model['tmpls']]

            compare_box.clear()
            compare_box.addItems(fields)

            card_box.clear()
            card_box.addItems(templates)

    def on_transfer_field_selected(self, row, box, name):
        field = box.currentText()
        if field:
            index = self.rows.index(row)
            self.transfer_rows[index][name] = field

    def transfer(self, **kwargs):
        self.console.append(f'query: deck:{self.selected_src_deck} card:{kwargs["src_card"]}')
        src_card_ids = mw.col.find_cards(f'deck:{self.selected_src_deck} card:{kwargs["src_card"]}')
        self.console.append(f'{len(src_card_ids)}')

        if len(src_card_ids):
            card = mw.col.get_card(src_card_ids[0])
            # result = mw.col.db.first('select * from revlog where cid= ?', src_card_ids[0])
            # result2 = mw.col.db.first('select * from cards where id= ?', src_card_ids[0])
            card_fields = ["type", "queue", "due", "ivl", "factor", "reps", "lapses", "left", "odue", "flags", "custom_data"]
            revlog_fields = ["ease", "ivl", "lastIvl", "factor", "time", "type"]
            revlog_fields_need_modified = ['id', 'cid', 'usn']
            result = mw.col.db.first('select {} from cards where id= ?'.format(', '.join(card_fields)), src_card_ids[0])
            card_fields = [getattr(card, f, None) for f in card_fields]
            breakpoint()


    def start(self):
        self.console.clear()
        for idx, row in enumerate(self.transfer_rows):
            if all(value != '' for value in row.values()):
                self.console.append(
                    f'Working on group {idx+1}')
                self.transfer(src_card=row["src_card"])
            else:
                self.console.append(
                    f'Skipping group {idx+1} because it has empty field'
                )


def showWindow():
    decks = mw.col.decks.allNames()
    models = [n.name for n in mw.col.models.all_names_and_ids()]
    mw.transferConfigWindow = TransferConfigWindow(decks, models)
    mw.transferConfigWindow.show()


# create a new menu item, "test"
action = QAction("Transfer Scheduling Data", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(showWindow)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
