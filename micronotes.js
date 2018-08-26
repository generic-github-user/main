const replace = function (string, substring_f, substring_r) {
      var substring_index;
      var output;
	do {
		substringIndex = string.indexOf(substring_f);
		output = string.replace(substring_f, substring_r);
	} while (substringIndex !== -1)
	return output;
}
