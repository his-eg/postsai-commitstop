export class Configuration {
    configText: string;
    changeComment: string;

    constructor( config: string, comment: string ) {
        this.configText = config;
        this.changeComment = comment;
    }

    sameAs( other: Configuration ): boolean {
        return this.configText === other.configText && this.changeComment === other.changeComment;
    }

    clone(): Configuration {
        return new Configuration( this.configText, this.changeComment );
    }

    toString() {
        return "<Configuration comment='" + this.changeComment + "'>";
    }
}