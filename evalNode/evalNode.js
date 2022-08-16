import ts from 'typescript'
const { transpile } = ts

import fs from 'fs'
const { readFileSync } = fs

const keypress = async () => {
	process.stdin.setRawMode(true)
	return new Promise(resolve => process.stdin.once('data', () => {
		process.stdin.setRawMode(false)
		resolve()
	}))
}
const messages = []
function alert(message) {
	messages.push(message)
}
(async () => {
	const data = readFileSync(process.argv[2], 'utf8')
	let result = transpile(data)
	let last = await eval(result)
	for (let message of messages) {
		console.log(message, "[Enter]",)
		await keypress()
	}
	if (last != undefined)
		console.log(last)
})().then(process.exit)
