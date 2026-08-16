from log.logging import logger
from data.data import ocr_result

class Edit_logic:
    def __init__(self, parent, db, filename, registered, name, description):
        self.parent = parent
        self.db = db
        self.filename = filename
        self.registered = registered
        self.name = name
        self.description = description
        self.open_window()

    def filling_data(self, registered, name):
        self.parent.edit.gui.lineEdit.setText(registered)
        self.parent.edit.gui.lineEdit_2.setText(name)

    def save_data(self):
        edit_registered = self.parent.edit.gui.lineEdit.text().strip()
        edit_name = self.parent.edit.gui.lineEdit_2.text().strip()
        return edit_registered, edit_name

    def open_window(self):
        self.parent.gui.pushButton_4.setEnabled(False)
        found_record = self.check_ki()
        if found_record:
            logger.debug(f"EDIT | Existing record has been found - {found_record}")
            self.filling_data(found_record[1], found_record[2])
        else:
            logger.debug(f"EDIT | Recognized entry has been found - {self.registered, self.name}")
            self.filling_data(self.registered, self.name)
        self.parent.edit.gui.pushButton.clicked.connect(self.save_record)
        self.parent.gui.pushButton_4.clicked.connect(self.save_db)

    def save_record(self):
        self.parent.gui.pushButton_4.setEnabled(True)
        self.edit_registered, self.edit_name = self.save_data()
        logger.debug(f"EDIT | Modified data has been preserved - {self.edit_registered, self.edit_name}")
        text = ocr_result(self.edit_registered, self.edit_name, self.description)
        self.parent.gui.plainTextEdit.setPlainText(text)
        self.parent.edit.close()

    def save_db(self):
        found_record = self.check_ki()
        print(found_record)
        if found_record:
            self.db.update_innovation_proposal_info(self.filename[:-4], self.edit_registered, self.edit_name)
            logger.debug(f"DOWNLOAD | In the DB, entry {found_record} was changed to entry {self.edit_registered, self.edit_name}")
        else:
            self.db.add_innovation_proposal_info(self.filename[:-4], self.edit_registered, self.edit_name, self.description)
            logger.debug(f"DOWNLOAD | A new record has been saved in the database - {self.edit_registered, self.edit_name}")
        
        self.parent.gui.pushButton_2.setEnabled(True)
    
    def check_ki(self):
        exist = self.db.get_innovation_proposal_info()
        logger.debug(f"{exist}")
        for i in exist:
            if i[0] == self.filename[:-4] and i[1] != None and i[2] != None:
                found_record = i
                return found_record
        



