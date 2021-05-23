function fish_prompt
	set_color normal
	set -l git_branch (git branch 2>/dev/null | sed -n '/\* /s///p')
	set_color $fish_color_param
	printf "%s:" (string replace -r '.*/([^/]+/[^/]+)$' '../$1' $PWD)
	set_color $fish_color_operator
	printf "%s{" (date "+%A@%l:%M%P")
	set_color purple
	echo -n "$git_branch"
	set_color $fish_color_operator
	echo -n '}'; set_color cyan
	echo -n  '$ '
end
