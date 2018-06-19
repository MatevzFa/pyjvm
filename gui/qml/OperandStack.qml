import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Styles 1.4

TableView {
	id: operandStack
	width: 400
	selectionMode: SelectionMode.NoSelection

	TableViewColumn {
		role: "active"
		width: 20
		movable: false
		resizable: false
	}

	TableViewColumn {
		role: "op"
		title: "Element"
		width: 100
		movable: false
		resizable: false
	}
}