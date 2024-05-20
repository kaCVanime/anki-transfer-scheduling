from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from .progress_gui import ProgressWindow


class TransferConfigWindow(QWidget):
    selected_src_deck = ""
    selected_target_deck = ""
    deck_list = []
    model_list = []
    rows = []
    transfer_rows = []
    canceled = False
    use_transfer_rev_log = False

    def __init__(self, deck_name_list, model_list):
        super(TransferConfigWindow, self).__init__()

        self.progress = ProgressWindow(mw)

        self.deck_list = deck_name_list
        self.model_list = model_list

        self.v_layout = QVBoxLayout(self)

        self.groupbox_deck = QGroupBox("1. Choose Deck")
        self.form_layout_deck = QFormLayout(self)
        self.combobox_src_deck = QComboBox(self)
        self.combobox_target_deck = QComboBox(self)

        self.scroll_area_rows = QScrollArea(self)
        self.groupbox_rows = QGroupBox("2. Add Group")
        self.v_layout_rows = QVBoxLayout(self)

        self.form_layout_rev_log = QFormLayout(self)
        self.checkbox_rev_log = QCheckBox(self)

        self.h_layout_row_btn = QHBoxLayout(self)
        self.add_row_btn = QPushButton(self)
        self.add_row_btn.setText("Add Group")
        self.remove_row_btn = QPushButton(self)
        self.remove_row_btn.setText("Remove Group")

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
        self.v_layout.addLayout(self.form_layout_rev_log)
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

        self.form_layout_rev_log.addRow(
            "Transfer Revision history", self.checkbox_rev_log
        )

        self.h_layout_row_btn.addWidget(self.remove_row_btn)
        self.h_layout_row_btn.addWidget(self.add_row_btn)

        self.setLayout(self.v_layout)

        self.start_btn.clicked.connect(lambda: self.start())
        self.add_row_btn.clicked.connect(lambda: self.add_row())
        self.remove_row_btn.clicked.connect(lambda: self.remove_row())
        self.checkbox_rev_log.stateChanged.connect(lambda: self.on_rev_log_checked())

    def combobox_init(self):
        self.combobox_src_deck.addItems(self.deck_list)
        self.combobox_src_deck.currentIndexChanged.connect(
            lambda: self.on_deck_selected(self.combobox_src_deck, "src")
        )
        self.on_deck_selected(self.combobox_src_deck, "src")
        self.combobox_target_deck.addItems(self.deck_list)
        self.combobox_target_deck.currentIndexChanged.connect(
            lambda: self.on_deck_selected(self.combobox_target_deck, "target")
        )
        self.on_deck_selected(self.combobox_target_deck, "target")

    def remove_row(self):
        if len(self.rows) > 1:
            row = self.rows.pop()
            self.transfer_rows.pop()
            self.v_layout_rows.removeWidget(row)
            row.deleteLater()

    def add_row(self):
        groupbox_row = QGroupBox("transfer group")
        h_layout_row = QHBoxLayout()

        groupbox_row_model = QGroupBox("1) Choose note type")
        form_layout_row_model = QFormLayout(self)
        combobox_src_model = QComboBox(self)
        combobox_target_model = QComboBox(self)

        groupbox_row_compare = QGroupBox("2) Choose comparing field")
        form_layout_row_compare = QFormLayout(self)
        combobox_src_compare_field = QComboBox(self)
        combobox_target_compare_field = QComboBox(self)

        groupbox_row_card = QGroupBox("3) Choose card template")
        form_layout_row_card = QFormLayout(self)
        combobox_src_card = QComboBox(self)
        combobox_target_card = QComboBox(self)

        groupbox_row.setLayout(h_layout_row)
        h_layout_row.addWidget(groupbox_row_model)
        h_layout_row.addWidget(groupbox_row_compare)
        h_layout_row.addWidget(groupbox_row_card)

        groupbox_row_model.setLayout(form_layout_row_model)
        form_layout_row_model.addRow("source", combobox_src_model)
        form_layout_row_model.addRow("target", combobox_target_model)

        groupbox_row_compare.setLayout(form_layout_row_compare)
        form_layout_row_compare.addRow("source", combobox_src_compare_field)
        form_layout_row_compare.addRow("target", combobox_target_compare_field)

        groupbox_row_card.setLayout(form_layout_row_card)
        form_layout_row_card.addRow("source", combobox_src_card)
        form_layout_row_card.addRow("target", combobox_target_card)

        combobox_src_model.addItems(self.model_list)
        combobox_src_model.currentIndexChanged.connect(
            lambda: self.on_model_selected(
                combobox_src_model, combobox_src_compare_field, combobox_src_card
            )
        )
        combobox_target_model.addItems(self.model_list)
        combobox_target_model.currentIndexChanged.connect(
            lambda: self.on_model_selected(
                combobox_target_model,
                combobox_target_compare_field,
                combobox_target_card,
            )
        )

        combobox_src_compare_field.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(
                groupbox_row, combobox_src_compare_field, "src_compare_field"
            )
        )
        combobox_target_compare_field.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(
                groupbox_row, combobox_target_compare_field, "target_compare_field"
            )
        )

        combobox_src_card.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(
                groupbox_row, combobox_src_card, "src_card"
            )
        )
        combobox_target_card.currentIndexChanged.connect(
            lambda: self.on_transfer_field_selected(
                groupbox_row, combobox_target_card, "target_card"
            )
        )

        self.v_layout_rows.addWidget(groupbox_row)
        self.rows.append(groupbox_row)
        self.transfer_rows.append(
            {
                "src_compare_field": "",
                "target_compare_field": "",
                "src_card": "",
                "target_card": "",
            }
        )
        self.on_model_selected(
            combobox_src_model, combobox_src_compare_field, combobox_src_card
        )
        self.on_model_selected(
            combobox_target_model, combobox_target_compare_field, combobox_target_card
        )

    def on_deck_selected(self, combobox, t):
        label = combobox.currentText()
        if t == "src":
            self.selected_src_deck = label
        else:
            self.selected_target_deck = label

    def on_rev_log_checked(self):
        if self.checkbox_rev_log.isChecked():
            self.use_transfer_rev_log = True
        else:
            self.use_transfer_rev_log = False

    def on_model_selected(self, model_box, compare_box, card_box):
        model_name = model_box.currentText()
        if model_name:
            model = mw.col.models.by_name(model_name)
            fields = mw.col.models.field_names(model)
            templates = [m["name"] for m in model["tmpls"]]

            compare_box.clear()
            compare_box.addItems(fields)

            card_box.clear()
            card_box.addItems(templates)

    def on_transfer_field_selected(self, row, box, name):
        field = box.currentText()
        if field:
            index = self.rows.index(row)
            self.transfer_rows[index][name] = field

    def transfer_card_info(self, src_card, target_cards):
        if len(target_cards):
            card_fields = [
                "type",
                "queue",
                "due",
                "ivl",
                "factor",
                "reps",
                "lapses",
                "left",
                "odue",
                "flags",
                "data",
            ]
            target_cids = [getattr(card, "id") for card in target_cards]
            sql = """
                UPDATE cards
                SET {f1}
                FROM (
                    SELECT {fields} FROM cards
                    WHERE id=? 
                ) as c1
                WHERE id IN ({tcids})
            """.format(
                f1=", ".join([f"{key}=c1.{key}" for key in card_fields]),
                fields=", ".join(card_fields),
                tcids=", ".join(map(str, target_cids)),
            )

            mw.col.db.execute(sql, getattr(src_card, "id"))

    def try_sql(self, sql):
        try:
            mw.col.db.execute(sql)
            return True
        except Exception:
            return False

    def transfer_revlog(self, src_card, target_cards):
        if len(target_cards):
            columns = ["id", "ease", "ivl", "lastIvl", "factor", "time", "type"]
            sql1 = "select {} from revlog where cid = ?".format(", ".join(columns))
            rev_result = mw.col.db.all(sql1, getattr(src_card, "id"))

            rows_delta = [0] * len(rev_result)
            for offset, card in enumerate(target_cards):
                cid = getattr(card, "id")

                delete_sql = "DELETE FROM revlog WHERE cid=?"
                mw.col.db.execute(delete_sql, cid)

                for idx, row in enumerate(map(list, rev_result)):
                    if rows_delta[idx] > 10:
                        self.console.append(
                            f'Transfer revision history failed. src cid: {getattr(src_card, "id")}. target cid: {cid}. {idx+1}th rev log'
                        )
                        continue

                    success = False
                    while not success and rows_delta[idx] <= 10:
                        sql = "INSERT INTO revlog(id,cid,usn,ease,ivl,lastIvl,factor,time,type) VALUES "
                        row[1:1] = [cid, -1]
                        row[0] = int(row[0]) + 1 + offset + rows_delta[idx]
                        sql += "(%s)" % ",".join(map(str, row))
                        success = self.try_sql(sql)
                        if not success:
                            rows_delta[idx] = rows_delta[idx] + 1
                    if not success:
                        self.console.append(
                            f'Transfer revision history failed. src cid: {getattr(src_card, "id")}. target cid: {cid}. {idx+1}th rev log'
                        )

    def update_progress(self, count):
        self.progress.update_labels(count)
        mw.app.processEvents()

    def transfer(
        self,
        title,
        src_card_tmpl,
        target_card_tmpl,
        src_compare_field,
        target_compare_field,
    ):
        src_card_ids = mw.col.find_cards(
            f"deck:{self.selected_src_deck} card:{src_card_tmpl} -is:new"
        )
        self.console.append(f"found {len(src_card_ids)} studied cards")

        if len(src_card_ids):
            self.progress.start(len(src_card_ids), 0)
            self.progress.update_title(title)
            for idx, cid in enumerate(src_card_ids):
                if self.progress.abort():
                    self.canceled = True
                    self.console.append("Canceld")
                    break

                self.update_progress(idx + 1)

                card = mw.col.get_card(cid)
                query = f"deck:{self.selected_target_deck} card:{target_card_tmpl} {target_compare_field}:{card.note()[src_compare_field]}"
                target_card_ids = mw.col.find_cards(query)
                target_cards = [mw.col.get_card(d) for d in target_card_ids]

                self.transfer_card_info(card, target_cards)
                if self.use_transfer_rev_log:
                    self.transfer_revlog(card, target_cards)

    def start(self):
        self.console.clear()
        self.canceled = False
        self.console.append("Start")
        for idx, row in enumerate(self.transfer_rows):
            if self.canceled:
                break
            if all(value != "" for value in row.values()):
                self.console.append(f"Processing Group {idx+1}")
                self.transfer(
                    f"Processing Group {idx+1}",
                    row["src_card"],
                    row["target_card"],
                    row["src_compare_field"],
                    row["target_compare_field"],
                )
                self.progress.finish()
            else:
                self.console.append(
                    f"Skipping group {idx+1} because it has empty field"
                )
        if not self.canceled:
            self.console.append("Done")


def show_window():
    decks = mw.col.decks.allNames()
    models = [n.name for n in mw.col.models.all_names_and_ids()]
    mw.transferConfigWindow = TransferConfigWindow(decks, models)
    mw.transferConfigWindow.show()


# create a new menu item, "test"
action = QAction("Transfer Scheduling Data", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(show_window)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
