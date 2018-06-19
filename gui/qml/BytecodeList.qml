import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.11


RowLayout {
    anchors.fill: parent
    spacing: 0
    Rectangle {
    	Layout.preferredWidth: parent.width / 2
        Layout.fillHeight: true
    }
    Rectangle {
	Layout.fillWidth: true
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
            }
            TableViewColumn {
            role: "op"
            title: "Opcode"
            width: 100
            }
            TableViewColumn {
            role: "operands"
            title: "Operands"
            width: 200
            }

            model: bytecode
        }

    }
}
