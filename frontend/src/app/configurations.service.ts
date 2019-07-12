import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import {Submission} from './submission'
import {Configuration} from './configuration'





function dateToStr( d: Date ) {
    return d.toLocaleString()
}

function formatDate( str: string ) {
    return dateToStr( new Date( str ) );
}

/*const MOCK = [
    new Submission( new Configuration( "conftext1", "confcomment1" ), "Karl-Heinz", formatDate( "2017-01-13" ) ),
    new Submission( new Configuration( "conftext2", "confcomment2" ), "Hans-Horst", formatDate( "2017-01-14" ) ),
    new Submission( new Configuration( "conftext3", "confcomment3" ), "Rüdiger-Maria", formatDate( "2017-01-15" ) )
];
*/

@Injectable()
export class ConfigurationsService {

    constructor( private httpClient: HttpClient ) { }

    private baseUrl = '../../api.py'; // TODO URL to web api

    private configurationsUrl = this.baseUrl + '?history=100';


    getConfigurations(): Observable<Submission[]> {
    	let confs = this.httpClient.get( this.configurationsUrl )
            .pipe( map(response => this.translate( response as any )));

        return confs;
    }

    private translate( o: string[][] ): Submission[] {
        let submissions = [];
        for ( var i = 0; i < o.length; i++ ) {
            var row = o[i];
            let conf = new Configuration( row[0], row[2] );
            let date = new Date(row[3]);
            let sumi = new Submission(conf , row[1], dateToStr(  date ), date.getTime() );
            submissions.push( sumi );
        }
        return submissions
    }

    saveConfig( submission: Configuration ): Observable<any> {
        // INSERT INTO `postsaidb`.`repository_status` (`configtext`, `username`, `changecomment`, `changetime`) VALUES ('+ oink', 'einer', '*kommentier*', '2004-01-23 17:00:00');        
        return this.httpClient.post( `${this.baseUrl}?activate=1`, submission, { headers: this.getHeaders(), responseType: 'text' });
    }


    private getHeaders() {
        let headers = new HttpHeaders();
        headers.append( 'Accept', 'application/json' );
        return headers;
    }
}