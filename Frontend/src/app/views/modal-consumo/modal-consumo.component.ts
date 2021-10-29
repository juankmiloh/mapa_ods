import { Component, OnInit, ViewChild } from '@angular/core';
import { MatBottomSheetRef } from '@angular/material/bottom-sheet';
import { MatSelectionList } from '@angular/material/list';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-modal-consumo',
  templateUrl: './modal-consumo.component.html',
  styleUrls: ['./modal-consumo.component.scss']
})
export class ModalConsumoComponent implements OnInit {
  @ViewChild('layers') listLayers: MatSelectionList;

  selectedLayers: string[]; // this array will contain the selected layers
  typesOfLayers: string[] = ['Usuarios residenciales', 'Usuarios no residenciales'];

  constructor(
    private dialogRef: MatBottomSheetRef<ModalConsumoComponent>,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {}

  selectLayers() {
    // console.log('selectedLayers -> ', this.listLayers._value);
    const option = this.listLayers._value;
    if (option) {
      this.dialogRef.dismiss(option[0]);
    } else {
      this.openSnackBar('Seleccione un sector', null, null, 'rigth');
    }
  }

  // Mostrar mensaje flotante en el footer de la pagina
  openSnackBar(message: string, action: string, duration?: number, hPosition?: any) {
    this.snackBar.open(message, action, {
      duration: duration ? duration : 2000,
      horizontalPosition: hPosition ? hPosition : 'bottom',
      verticalPosition: 'bottom',
    });
  }

}
