import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';


import {Submission} from './submission'
import {Configuration} from './configuration'





function dateToStr( d: Date ) {
    return d.toLocaleString()
}

function formatDate( str: string ) {
    return dateToStr( new Date( str ) );
}

const MOCK = [
    new Submission( new Configuration( "conftext1", "confcomment1" ), "Karl-Heinz", formatDate( "2017-01-13" ) ),
    new Submission( new Configuration( "conftext2", "confcomment2" ), "Hans-Horst", formatDate( "2017-01-14" ) ),
    new Submission( new Configuration( "conftext3", "confcomment3" ), "Rüdiger-Maria", formatDate( "2017-01-15" ) )
];


@Injectable()
export class ConfigurationsService {

    constructor( private http: Http ) { }

    private baseUrl = '../../api.py'; // TODO URL to web api

    private configurationsUrl = this.baseUrl + '?history=100';


    getConfigurations(): Promise<Submission[]> {
        let mock = false;
        if ( mock )
            return Promise.resolve( MOCK ).then( x => x );


        let confs = this.http.get( this.configurationsUrl )
            .toPromise()
            .then( response =>
                this.translate( response.json() )
            )
            .catch( this.handleError );

        return confs
    }

    private translate( o: string[][] ): Submission[] {
        let submissions = [];
        for ( var i = 0; i < o.length; i++ ) {
            var row = o[i];
            let sumi = new Submission( new Configuration( row[0], row[2] ), row[1], dateToStr( new Date( row[3] ) ) );
            submissions.push( sumi );
        }
        return submissions
    }

    private handleError( error: any ): Promise<any> {
        alert( 'error retrieving data: ' + error )
        return Promise.reject( error.message || error );
    }


    saveConfig( submission: Configuration ): Promise<Response> {
        // INSERT INTO `postsaidb`.`repository_status` (`configtext`, `username`, `changecomment`, `changetime`) VALUES ('+ oink', 'einer', '*kommentier*', '2004-01-23 17:00:00');        
        // this won't actually work because the StarWars API doesn't 
        // is read-only. But it would look like this:
        console.error( submission.toString() );
        return this.http.post( `${this.baseUrl}?activate=1`, JSON.stringify( submission ), { headers: this.getHeaders() }).toPromise();
    }


    private getHeaders() {
        let headers = new Headers();
        headers.append( 'Accept', 'application/json' );
        return headers;
    }
}