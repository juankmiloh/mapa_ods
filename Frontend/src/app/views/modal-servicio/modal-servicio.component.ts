import { Component, OnInit } from '@angular/core';

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

  constructor() { }

  ngOnInit(): void {
  }

}
