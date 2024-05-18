from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *


class TransferConfigWindow(QWidget):
    selected_src_deck = ""
    selected_target_deck = ""
    selected_src_field = ""
    selected_target_field = ""
    deck_list=[]
    model_list=[]
    src_field_list=[]
    target_field_list=[]
    card_rows = []

    def __init__(self, deck_name_list, model_list):
        super(TransferConfigWindow, self).__init__()
        self.deck_list = deck_name_list
        self.model_list = model_list
        self.combobox_src_deck = QComboBox(self)
        self.combobox_target_deck = QComboBox(self)
        self.combobox_src_field = QComboBox(self)
        self.combobox_target_field = QComboBox(self)

        self.start_btn = QPushButton(self)
        self.start_btn.setText("Start")
        self.console = QTextEdit(self)
        self.v_layout = QFormLayout(self)
        self.layout_init()
        self.combobox_init()

        if not len(deck_name_list):
            showInfo("there is no deck in your collection")

    def layout_init(self):
        self.v_layout.addRow("Select source deck:", self.combobox_src_deck)
        self.v_layout.addRow("Select target deck:", self.combobox_target_deck)
        self.v_layout.addRow("Select comparing field from source deck:", self.combobox_src_field)
        self.v_layout.addRow("Select comparing field from target deck:", self.combobox_target_field)
        self.v_layout.addRow(self.start_btn)
        self.v_layout.addRow(self.console)
        self.setLayout(self.v_layout)
        self.start_btn.clicked.connect(lambda: self.start())

    def combobox_init(self):
        self.combobox_src_deck.addItems(self.deck_list)
        self.combobox_src_deck.currentIndexChanged.connect(lambda: self.on_deck_selected(self.combobox_src_deck, 'src'))
        self.combobox_target_deck.addItems(self.deck_list)
        self.combobox_target_deck.currentIndexChanged.connect(lambda: self.on_deck_selected(self.combobox_target_deck, 'target'))


    def on_deck_selected(self, combobox, type):
        label = combobox.currentText()
        if type == 'src':
            self.selected_src_deck = label
        else:
            self.selected_target_deck = label
        self.update_compare_field_options(type, label)

    def clear_card_rows(self):
        for item in self.card_rows:
            label = self.v_layout.labelForField(item.component)
            if label is not None:
                label.deleteLater()
            item.component.deleteLater()
    def add_card_rows(self, templates):
        for template in templates:
            combox_src = QComboBox(self)

    def update_compare_field_options(self, type, label):
        nids = mw.col.find_notes(f'deck:"{label}"')
        if len(nids):
            combobox = self.combobox_src_field if type == 'src' else self.combobox_target_field
            combobox = self.combobox_src_field if type == 'src' else self.combobox_target_field
            combobox.clear()
            note = mw.col.get_note(nids[0])
            model = note.note_type()
            # self.add_card_rows(model['tmpls'])
            # keys = [m["name"] for m in model['tmpls']]
            keys = note.keys()
            for key in keys:
                combobox.addItem(key)
        else:
            showInfo(f'deck {self.selected_src_deck if type == "src" else self.selected_target_deck } has no card')

    def start(self):
        pass




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