import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Styles 1.4


RowLayout {
    anchors.fill: parent
    spacing: 5

    Component.onCompleted: {
		bytecodeTable.selection.clear()
		var loc = app.getCurLoc(5)
		bytecodeTable.selection.select(loc)
		bytecodeTable.positionViewAtRow(loc, ListView.Center)
	}

    Rectangle {
    	id: col1
		Layout.preferredWidth: 480
		Layout.fillHeight: true

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
	}

    Rectangle {
    	id: col2
		Layout.fillWidth: true
		Layout.fillHeight: true

		ColumnLayout {

			spacing: 10

			Button {
				Layout.fillWidth: true
				text: "Step"
				onClicked: {
					app.stepExecutor()
					bytecodeTable.selection.clear()
					var loc = app.getCurLoc(5)
					bytecodeTable.selection.select(loc)
					bytecodeTable.positionViewAtRow(loc, ListView.Center)
				}
			}
			Button {
				Layout.fillWidth: true
				text: "Step Out"
				onClicked: {
					app.stepOut()
					bytecodeTable.selection.clear()
					var loc = app.getCurLoc(5)
					bytecodeTable.selection.select(loc)
					bytecodeTable.positionViewAtRow(loc, ListView.Center)
				}
			}


			Separator {}

			Label {
				text: "Frame"
				font.pixelSize: 20
			}
			Text {
				text: frameInfo
			}
			Separator {}

			Label {
				text: "Operand stack"
				font.pixelSize: 20
			}
			OperandStack {
				Layout.fillWidth: true
			}
			Separator {}
		}

    }
}
