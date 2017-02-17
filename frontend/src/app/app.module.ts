import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { NgxDatatableModule } from '@swimlane/ngx-datatable';

import { ConfigurationsService } from './configurations.service';


import { AppComponent } from './app.component';
@NgModule( {
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        NgxDatatableModule
    ],
    providers: [ConfigurationsService],
    bootstrap: [AppComponent]
})
export class AppModule { }
