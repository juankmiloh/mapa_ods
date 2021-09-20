import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-modal-servicio',
  templateUrl: './modal-servicio.component.html',
  styleUrls: ['./modal-servicio.component.scss']
})
export class ModalServicioComponent implements OnInit {

  centered = false;
  disabled = false;
  unbounded = false;

  radius: number;
  color: string;

  constructor(
    private dialogRef: MatDialogRef<ModalServicioComponent>,
  ) { }

  ngOnInit(): void {
  }

  setServicio(servicio) {
    const data = {modal: 'servicio', value: servicio};
    this.dialogRef.close(data);
  }
}
