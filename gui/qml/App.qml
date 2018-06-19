import QtQuick 2.6
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Styles 1.4


RowLayout {
    anchors.fill: parent
    spacing: 5

    Rectangle {
		Layout.preferredWidth: 480
		Layout.fillHeight: true

		Bytecode {}
	}

    Rectangle {
    	id: col2
		Layout.fillWidth: true
		Layout.fillHeight: true

		ColumnLayout {

			spacing: 10

			Button {
				Layout.fillWidth: true
				id: stepButton
				text: "Step"
				onClicked: app.stepExecutor()
			}

			Separator {}

			Label {
				text: "Frame"
				font.pixelSize: 20
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
