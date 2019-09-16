(defun async-shell-command-no-window
    (command)
  (interactive)
  (let
      ((display-buffer-alist
        (list
         (cons
          "\\*Async Shell Command\\*.*"
          (cons #'display-buffer-no-window nil)))))
    (async-shell-command
     command)))

(defun mpw (site)
  "MasterPassword algorithm now in emacs.
Note that mpw need to be installed and full name configured for this function to work."
  (interactive "sSite: ")
  (async-shell-command-no-window (concat "mpw --quiet \"" site "\""))
  )

