import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Styles 1.4

TableView {
	id: bytecodeTable
	width: 400
	selectionMode: SelectionMode.NoSelection
	anchors.fill: parent

	TableViewColumn {
		role: "loc"
		title: "loc"
		width: 100
		movable: false
		resizable: false
	}
	TableViewColumn {
		role: "op"
		title: "Opcode"
		delegate: Text {
			text: styleData.value
			font.family: "monospace"
		}
		width: 150
		movable: false
		resizable: false
	}
	TableViewColumn {
		role: "operands"
		title: "Operands"
		width: 200
		movable: false
		resizable: false
	}

	model: bytecode
}