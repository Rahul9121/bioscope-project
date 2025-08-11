module.exports = function override(config, env) {
  config.module.rules.forEach((rule) => {
    if (rule.oneOf) {
      rule.oneOf.forEach((one) => {
        if (one.use) {
          one.use = one.use.filter(
            (use) => !(typeof use === "object" && use.loader.includes("postcss-loader"))
          );
        }
      });
    }
  });
  return config;
};
