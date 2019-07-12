import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgxDatatableModule } from '@swimlane/ngx-datatable';

import { ConfigurationsService } from './configurations.service';


import { AppComponent } from './app.component';
@NgModule( {
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserAnimationsModule,
        FormsModule,
        HttpClientModule,
        NgxDatatableModule
    ],
    providers: [ConfigurationsService],
    bootstrap: [AppComponent]
})
export class AppModule { }
