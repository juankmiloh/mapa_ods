import { Component, OnInit, ViewChild } from '@angular/core';
import { MatBottomSheetRef } from '@angular/material/bottom-sheet';
import { MatSelectionList } from '@angular/material/list';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-modal-estratificacion',
  templateUrl: './modal-estratificacion.component.html',
  styleUrls: ['./modal-estratificacion.component.scss'],
})
export class ModalEstratificacionComponent implements OnInit {
  @ViewChild('layers') listLayers: MatSelectionList;

  selectedLayers: string[]; // this array will contain the selected layers
  typesOfLayers: string[] = ['Estratos registrados por el prestador iguales a los de la alcaldía', 'Estratos registrados por el prestador diferentes a los de la alcaldía', 'Estratos registrados por el prestador sin registro en alcaldía'];

  constructor(
    private dialogRef: MatBottomSheetRef<ModalEstratificacionComponent>,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {}

  selectLayers() {
    // console.log('selectedLayers -> ', this.listLayers._value);
    const option = this.listLayers._value;
    if (option) {
      this.dialogRef.dismiss(option[0]);
    } else {
      this.openSnackBar('Seleccione una opción de estratificación', null, null, 'rigth');
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
