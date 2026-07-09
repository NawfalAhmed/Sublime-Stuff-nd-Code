const fs = require('fs');
const { execSync } = require('child_process');
const {
  prompt,
} = require('/Users/nawfal.ahmed/.config/yarn/global/node_modules/enquirer');

const filePath = '/Users/nawfal.ahmed/Sublime/goToFolderOutput.txt';

const goToFolder = async (folderToFind) => {
  try {
    // Use find command to search for the folders
    const foundFolders = execSync('find . -type d -name ' + folderToFind, {
      encoding: 'utf-8',
    })
      .trim()
      .split('\n')
      .filter((name) => name !== '');

    if (foundFolders.length > 0) {
      // If only one folder is found, cd to it directly
      if (foundFolders.length === 1) {
        fs.writeFile(filePath, foundFolders[0], () => {});
      } else {
        // Ask the user to choose a folder
        const { selectedFolder } = await prompt({
          type: 'select',
          name: 'selectedFolder',
          message: 'Select a folder:',
          choices: foundFolders,
        });
        fs.writeFile(filePath, selectedFolder, () => {});
      }
    } else {
      console.log('Folder not found: ' + folderToFind);
      fs.writeFile(filePath, '.', () => {});
    }
  } catch (error) {
    console.error('An error occurred:', error.message);
  }
};
goToFolder(process.argv[2]);
