package be.inqa.phd.hivhack.data;

import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlProperty;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class GazetteNotice {

	 @JacksonXmlProperty(localName = "text")
	    private String text;
}
