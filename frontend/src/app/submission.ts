import { Configuration } from './configuration'

export class Submission {
    config: Configuration;
    username: string;
    changetime: string;
    timestamp : number;
 

    constructor( config: Configuration, user: string, time: string, timestamp:number ) {
        this.config = config;
        this.username = user;
        this.changetime = time;
        this.timestamp = timestamp;
    }

    toString() {
        return "<Submission from " + this.changetime + " by " + this.username + ": " + this.config + ">";
    }
}