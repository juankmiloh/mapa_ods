import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './views/home/home.component';
import { MapInterrupcionComponent } from './views/map-interrupcion/map-interrupcion.component';


const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'map-page', component: MapInterrupcionComponent },
  { path: 'ods', redirectTo: '/map-page', pathMatch: 'full' },
  { path: 'ods/&gtjwt', redirectTo: '/map-page', pathMatch: 'full' },
  { path: '', redirectTo: '/map-page', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
