$('document').ready(function() {
	var url = '/repos',
		w = 1360,
		h = 560,
		svg = d3.select('div.repovis')
				.append('svg')
				.attr('viewBox', '0 0 ' + w + ' ' + h)
				.attr('preserveAspectRatio', 'xMidYMid meet'),
		radiusScale = d3.scale.sqrt().range([1, 140]),
		colorScale = d3.scale.category10();

	function charge(d) {
		return radiusScale(d.value) * radiusScale(d.value) * -0.135;
	}

	var force = d3.layout.force()
		.gravity(0.1)
		.distance(5)
		.charge(charge)
		.size([w, h])
		.alpha(0.3);

	d3.json(url, function(error, data) {
		data = data.sort(function(a, b){ return d3.descending(a.value, b.value) });
		var maxValue = parseInt(data[0].value),
			topTenLanguages = new Array(),
			totalSum = d3.sum(data, function(d) {
				return d.value
			}),
			g = svg.append('g').attr('transform', 'translate(0, 0)');

		for (var i = 0; i < 10; i++)
			topTenLanguages.push(data[i]);

		var circles = g.selectAll('circle')
			.data(data)
			.enter()
			.append('circle')
			.attr('fill', 'black');

		var tip = d3.tip()
			.attr('class', 'd3-tip')
			.offset([-10, 0])
			.html(function(d) {
				return "<strong>Language: </strong> " + d.language + "</span>" +
					   "<br /><strong>Used %: </strong> " + ((d.value / totalSum) * 100).toFixed(2) + '%';
			});

		svg.call(tip);
		force.nodes(data);
		radiusScale.domain([1, maxValue])

		force.on("tick", function() {
			force.alpha(0.1);
			circles
				.attr("cx", function(d) {
					return d.x
				})
				.attr("cy", function(d) {
					return d.y
				})
				.attr("r", function(d) {
					return radiusScale(d.value);
				})
				.attr('fill', function(d, i) {
					if (i < 10)
						return colorScale(i);
					return 'rgb(138, 137, 166)';
				})
				.on('mouseover', tip.show)
				.on('mouseout', tip.hide)
				.call(force.drag);
		});

		force.start();
		svg = d3.select('div.top-langs')
				.append('svg')
				.attr('viewBox', '0 0 1800 50')
				.attr('preserveAspectRatio', 'xMidYMid meet');
		g = svg.append('g').attr('transform', 'translate(60, 0)');
		g.selectAll('rect')
		 .data(topTenLanguages)
		 .enter()
		 .append('rect')
		 .attr('x', function(d, i){ return 160 * i + 30})
		 .attr('y', 10)
		 .attr('width', 20)
		 .attr('height', 20)
		 .style('fill', function(d, i){ return colorScale(i); });

		g.selectAll('text')
		 .data(topTenLanguages)
		 .enter()
		 .append('text')
		 .attr('x', function(d, i){ return 160 * i + 60})
		 .attr('y', 28)
		 .text(function(d, i){
		 	return d.language;
		 })
		 .style('font-size', '22px');

		$('div.overlay').attr('style', 'display: none');
	});
});