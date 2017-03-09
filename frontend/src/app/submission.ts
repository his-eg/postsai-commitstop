import { Configuration } from './configuration'

export class Submission {
    config: Configuration;
    username: string;
    changetime: string;

    constructor( config: Configuration, user: string, time: string ) {
        this.config = config;
        this.username = user;
        this.changetime = time;
    }

    toString() {
        return "<Submission from " + this.changetime + " by " + this.username + ": " + this.config + ">";
    }
}