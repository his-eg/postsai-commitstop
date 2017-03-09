import { Component } from '@angular/core';
import { OnInit } from '@angular/core';

import { Configuration } from './configuration';
import { Submission } from './submission';

import { ConfigurationsService } from './configurations.service';

@Component( {
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

    constructor( private configurationsService: ConfigurationsService ) { }

    ngOnInit(): void {
        this.fetchConfigs();

    }


    setRows( rows: Submission[] ) {
        this.rows = rows;
        if ( rows.length > 0 ) {
            this.currentConfig = rows[0].config.clone();
            this.selected = [rows[0]];
        }
    }

    fetchConfigs(): void {
        this.configurationsService.getConfigurations().then( rows => {
            this.setRows( rows );
        });
    }

    title = 'Postsai Commit Permissions';

    currentConfig = new Configuration( "- .* .* .* .*", "comment" );

    rows: Submission[];

    columns = [
        { prop: 'changetime', name: 'Activation Date', sortable: false },
        { prop: 'username', name: 'User', sortable: false },
        { prop: 'config.changeComment', name: 'Comment', sortable: false }
    ];

    selected: Submission[] = [];

    onSelect( event ) {
        if ( this.selected.length > 0 )
            this.currentConfig = this.selected[0].config.clone();
    }

    doSubmit( event ) {
        if ( this.rows.length > 0 && this.currentConfig.sameAs( this.rows[0].config ) )
            alert( "Not saved. Configuration is already active." );
        else if ( confirm( "Save new configuration?" ) ) {
            let ths = this;
            let added = this.currentConfig.clone();
            this.configurationsService.saveConfig( added ).then(
                function( data ) {
                    return ths.configurationsService.getConfigurations()
                }
            ).then( rows => {
                ths.setRows( rows );
            },
                function( data ) {
                    alert( "Could not save configuration.\n\nMessage returned by server: '" + data + "'" );
                });
        }
    }
}
