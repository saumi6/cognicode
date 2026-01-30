"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const axios_1 = require("axios");
const path = require("path");
// Output channel for logging
let outputChannel;
// Terminal for running tests
let testTerminal;
// Hardcoded paths for reliability
const PROJECT_ROOT = "C:\\Users\\gurav\\prog\\college\\BE Proj\\cognicode";
const PYTHON_PATH = `${PROJECT_ROOT}\\myenv\\Scripts\\python.exe`;
const TEST_SCRIPT_PATH = `${PROJECT_ROOT}\\test.py`;
function activate(context) {
    outputChannel = vscode.window.createOutputChannel("CogniCode");
    outputChannel.show(true);
    outputChannel.appendLine("CogniCode Client Active! 🚀");
    outputChannel.appendLine(`Using Python: ${PYTHON_PATH}`);
    outputChannel.appendLine("Listening for file changes...");
    // Register Save Event
    let disposable = vscode.workspace.onDidSaveTextDocument(async (document) => {
        if (document.languageId === 'python') {
            await handleFileSave(document);
        }
    });
    context.subscriptions.push(disposable);
}
async function handleFileSave(document) {
    const filePath = document.fileName;
    outputChannel.appendLine(`\n[Event] Saved: ${path.basename(filePath)}`);
    try {
        // 1. Notify Server
        const serverUrl = 'http://localhost:8000/impact/file';
        outputChannel.appendLine(`[Query] Asking CogniServer for impact analysis...`);
        const response = await axios_1.default.post(serverUrl, {
            file_path: filePath
        });
        const data = response.data;
        let impactedFiles = data.affected_files;
        // Sort files: The triggered file should be FIRST, then the rest
        // Remove the triggered file if it exists in the list, then unshift it to the front
        impactedFiles = impactedFiles.filter(f => f !== filePath);
        impactedFiles.unshift(filePath);
        if (impactedFiles.length === 0) {
            outputChannel.appendLine("✅ No dependent files found. No tests to run.");
            return;
        }
        outputChannel.appendLine(`⚠️ Impact Detected! The following files may be broken:`);
        impactedFiles.forEach(f => outputChannel.appendLine(`   - ${path.basename(f)}`));
        // 2. Run Tests
        runTests(impactedFiles);
    }
    catch (error) {
        outputChannel.appendLine(`❌ Error connecting to CogniServer: ${error.message}`);
        outputChannel.appendLine("Make sure the server is running: 'python -m uvicorn cogniserver.main:app'");
    }
}
function runTests(filesToTest) {
    // Ensure we have a terminal
    if (!testTerminal || testTerminal.exitStatus) {
        testTerminal = vscode.window.createTerminal("CogniTest Runner");
    }
    testTerminal.show();
    outputChannel.appendLine(`[Action] Queueing tests for ${filesToTest.length} files...`);
    // Run commands separately so they don't block each other if one fails (unless user wants fail-fast)
    // Sending them as separate terminal lines ensures they run sequentially but independently
    filesToTest.forEach(file => {
        const cmd = `"${PYTHON_PATH}" "${TEST_SCRIPT_PATH}" "${file}"`;
        testTerminal.sendText(cmd); // Queue command
    });
}
function deactivate() {
    if (testTerminal) {
        testTerminal.dispose();
    }
}
//# sourceMappingURL=extension.js.map