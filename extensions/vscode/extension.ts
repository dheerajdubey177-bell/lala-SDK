import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    const serverOptions: ServerOptions = {
        run: { command: "lala", args: ["lsp"] },
        debug: { command: "lala", args: ["lsp"] }
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'lala' }]
    };

    client = new LanguageClient(
        'lalaLanguageServer',
        'Lala Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
