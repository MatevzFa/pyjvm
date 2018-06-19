import QtQuick 2.6
import QtQuick.Controls 1.4

TableView {

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
    	width: 100
    }

    model: bytecode
}