import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-modal-capas',
  templateUrl: './modal-capas.component.html',
  styleUrls: ['./modal-capas.component.scss']
})
export class ModalCapasComponent implements OnInit {

  typesOfShoes: string[] = ['Consumos', 'Calidad del servicio', 'Estratificación'];

  constructor() { }

  ngOnInit(): void {
  }

}
