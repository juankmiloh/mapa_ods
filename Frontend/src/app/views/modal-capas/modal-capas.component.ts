import { Component, OnInit, ViewChild } from '@angular/core';
import { MatBottomSheet } from '@angular/material/bottom-sheet';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSelectionList } from '@angular/material/list';
import { ModalConsumoComponent } from '../modal-consumo/modal-consumo.component';
import { ModalEstratificacionComponent } from '../modal-estratificacion/modal-estratificacion.component';

@Component({
  selector: 'app-modal-capas',
  templateUrl: './modal-capas.component.html',
  styleUrls: ['./modal-capas.component.scss'],
})
export class ModalCapasComponent implements OnInit {
  @ViewChild('layers') listLayers: MatSelectionList;

  selectedLayers: string[]; // this array will contain the selected layers
  typesOfLayers: string[] = ['Consumos', 'Estratificación', 'Calidad del servicio'];
  bottomSheetRef: any; // modal tipos de usuario
  @ViewChild('layers') listSidenav: MatSelectionList;

  constructor(
    private dialogRef: MatDialogRef<ModalCapasComponent>,
    private bottomSheet: MatBottomSheet,
  ) { }

  ngOnInit(): void {
    const loadData = JSON.parse(localStorage.getItem('capas'));
    if (loadData) {
      this.selectedLayers = [loadData.capa.charAt(0).toUpperCase() + loadData.capa.slice(1)];
    }
  }

  selectLayers() {
    // console.log('selectedLayers -> ', this.listLayers._value[0]);
    const options = this.listLayers._value[0];
    if (options === 'Consumos') {
      this.openBottomSheet();
      this.listSidenav.deselectAll();
    } else if (options === 'Estratificación') {
      this.openBottomSheetEstratificacion();
      this.listSidenav.deselectAll();
    }
  }

  // Mostrar modal de consumos
  openBottomSheet(): void {
    this.bottomSheetRef = this.bottomSheet.open(ModalConsumoComponent, {
      data: {}, // Se pasan valores al modal
      panelClass: 'custom-width',
      // disableClose: true
    });

    // subscribe to observable que se ejecuta despues de cerrar el modal, obtiene los valores del hijo
    this.bottomSheetRef.afterDismissed().subscribe(async (dataFromChild: any) => {
      // console.log('valores enviados del hijo', dataFromChild);
      let codOption = null;
      if (dataFromChild === 'Usuarios residenciales') {
        codOption = 1;
      } else if (dataFromChild === 'Usuarios no residenciales') {
        codOption = 2;
      }
      if (codOption !== null) {
        const data = {modal: 'capas', value: {capa: 'consumos', option: {cod: codOption, nombre: dataFromChild}}};
        this.dialogRef.close(data);
      }
    });
  }

  // Mostrar modal de estratos
  openBottomSheetEstratificacion(): void {
    this.bottomSheetRef = this.bottomSheet.open(ModalEstratificacionComponent, {
      data: {}, // Se pasan valores al modal
      panelClass: 'custom-width',
      // disableClose: true
    });

    // subscribe to observable que se ejecuta despues de cerrar el modal, obtiene los valores del hijo
    this.bottomSheetRef.afterDismissed().subscribe(async (dataFromChild: any) => {
      console.log('valores enviados del hijo', dataFromChild);
      let codOption = null;
      if (dataFromChild === 'Estratos registrados por el prestador iguales a los de la alcaldía') {
        codOption = 1;
      } else if (dataFromChild === 'Estratos registrados por el prestador diferentes a los de la alcaldía') {
        codOption = 2;
      } else if (dataFromChild === 'Estratos registrados por el prestador sin registro en alcaldía') {
        codOption = 3;
      }
      if (codOption !== null) {
        const data = {modal: 'capas', value: {capa: 'estratificacion', option: {cod: codOption, nombre: dataFromChild}}};
        this.dialogRef.close(data);
      }
    });
  }

}
