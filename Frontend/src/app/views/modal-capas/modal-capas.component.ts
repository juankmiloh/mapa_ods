import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSelectionList } from '@angular/material/list';

@Component({
  selector: 'app-modal-capas',
  templateUrl: './modal-capas.component.html',
  styleUrls: ['./modal-capas.component.scss']
})
export class ModalCapasComponent implements OnInit {
  @ViewChild('layers') listLayers: MatSelectionList;

  selectedLayers: string[]; // this array will contain the selected layers
  typesOfLayers: string[] = ['Consumos', 'Calidad del servicio', 'Estratificación'];

  constructor(
    private dialogRef: MatDialogRef<ModalCapasComponent>,
  ) { }

  ngOnInit(): void {
    const loadData = JSON.parse(localStorage.getItem('capas'));
    this.selectedLayers = loadData;
  }

  selectLayers() {
    // console.log('selectedLayers -> ', this.listLayers._value);
    const options = this.listLayers._value;
    const data = {modal: 'capas', value: options};
    this.dialogRef.close(data);
  }

}
